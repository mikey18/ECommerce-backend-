from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from accounts.serializers import *
from .models import Cart

# Create your views here.
class UploadCartAPI(APIView):
    def post(self, request):
        token = request.COOKIES.get('pppit')

        data = request.data
        # serializer = CartSerializer(data)

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired')

        user = User.objects.filter(id=payload['id']).first()
        # serializer = UserSerializer(user)

        cart = Cart.objects.filter(email=user.email).first()
        cartnumber = str(int(cart.cartnumber) + data['cartnumber'])
        cart.cartnumber = cartnumber
        cart.save()
        # print(cart.email)
        
        return Response({
            'status': 200,
            'message': 'Added to cart'
        })



