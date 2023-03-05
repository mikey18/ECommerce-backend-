from django.urls import path
from .views import GetProductsAPI

urlpatterns = [
    path('', GetProductsAPI.as_view())
]