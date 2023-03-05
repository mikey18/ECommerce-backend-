from django.urls import path
from .views import UploadCartAPI

urlpatterns = [
    path("carty/", UploadCartAPI.as_view())
]