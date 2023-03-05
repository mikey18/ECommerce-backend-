from django.urls import path
from .views import RegisterAPI, VerifyOTP, LoginAPI, UserViewAPI, LogOutAPI
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('login/', LoginAPI.as_view()),
    path('user/', UserViewAPI.as_view()),
    path('logout/', LogOutAPI.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]