from django.urls import path
from .views import (
    Sign_up_api,
    SigninAPIView,
    SignoutAPIView,
    PasswordChangeAPIView,
    UserProfileUpdateAPIView,
)

urlpatterns = [
    path('sign-up/', Sign_up_api.as_view(), name='sign-up'),
    path('sign-in/', SigninAPIView.as_view(), name='sign-in'),
    path('sign-out/', SignoutAPIView.as_view(), name='sign-out'),
    path('change-password/', PasswordChangeAPIView.as_view(), name='change-password'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
]
