from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

class GetProductsAPI(APIView):
    def get(self, request):
        try:
            id = request.query_params["id"]
            if id != None:
                product = Product.objects.get(id=id)
                serializer = ProductSerializer(product)
        except:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)

        return Response({
            'status': 200,
            'data': serializer.data
        })