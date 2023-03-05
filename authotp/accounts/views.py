from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .emails import send_otp
from .models import User, Token
from user_profile.models import Cart 
import jwt, datetime

class RegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                email = serializer.data['email']

                user = User.objects.get(email=email)
                send_otp(user)


                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                
                return Response({
                    'status': 200,
                    'message': 'User successfully registered check email',
                    'data': serializer.data,
                    'token': token
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)

            if serializer.is_valid():
                jwt_email = serializer.data['otpemail']
                otp = serializer.data['otp']

                payload = jwt.decode(jwt_email, 'secret', algorithms=['HS256'])
                user_token_id = Token.objects.get(email=payload['id'])
                user_token_email = user_token_id.email

                user = User.objects.filter(email=user_token_email).first()

                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'invalid email'
                    })

                if  otp != user_token_id.otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'wrong otp'
                    })

                if user.is_verified == True:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'User already verified'
                    })

                user.is_verified = True
                user.save()
                Cart.objects.create(email=user_token_email, items=0)
                user_token_id.delete()

                return Response({
                    'status': 200,
                    'message': 'Account verified',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)

class LoginAPI(APIView):
    def post(self, request):
        serializer = LogInSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = User.objects.filter(email=email).first()

            if user is None:
                return Response({
                    'message':'Incorrect email or password'
                })
            if not user.check_password(password):
                return Response({
                    'message':'Invaild email or password'
                })
            if user.is_verified == False:
                return Response({
                    'message':'User not verified'
                })
          
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'my_fucking_secret_key', algorithm='HS256')
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='pppit', value=token, httponly=True)
        
            response.data = {
                'status': 200,
                'message': "Login successful",
                'jwt': token,
                "permisssion": "regular user"
            }
            return response
        else:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
              
class UserViewAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        token = request.COOKIES.get('pppit')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'my_fucking_secret_key', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired')


        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        
        return Response({
            'status': 200,
            'data': serializer.data,
            'jwt': token,
            'user_type': 'user',
            # 'user_type': 'seller',
        })

class LogOutAPI(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('pppit')

        response.data = {
            "message": "Logout Successful",
            "status": 200
        }

        return response

# class ResetPasswordAPI(APIView):
#     def post(self, request):



