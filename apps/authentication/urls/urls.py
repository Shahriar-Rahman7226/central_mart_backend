from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.authentication.views.views import *

urlpatterns = [
    # JWT Token
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),

    # Login & Logout
    path("login/", LoginViewSet.as_view({'post': 'create'}), name='login'),
    path("logout/", LogoutViewSet.as_view({'post': 'create'}), name='logout'),

    # Reset Password
    path("reset-password/", ResetPasswordViewSet.as_view({'post': 'create'}), name='reset_password'),

    # Forget Password
    path("forget-password/", ForgetPasswordViewSet.as_view({'post': 'get_forget_password_mail'}), name='forget_password'),
    path("confirm-password/<uidb64>/<token>/", ForgetPasswordViewSet.as_view({'post': 'create_new_password'}), name="confirm_password"),
]