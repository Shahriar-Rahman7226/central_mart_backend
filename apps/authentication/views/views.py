import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.serializers import *
from external.time_checker import time_checker
from apps.users.models import UserModel
from rest_framework import status
from external.send_message import send_email, send_sms
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

@extend_schema(tags=['Authentication Token'])
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(tags=['Authentication'])
class LoginViewSet(ModelViewSet):
    model_class = UserModel
    permission_classes = []
    serializer_class = LoginSerializer

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', None)
        password = request.data.get('password', None)

        if not phone_number or not password:
            return Response({'message': 'Phone number and password is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = self.model_class.objects.filter(phone_number=phone_number).first()

        if not instance:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.login_attempt >= 5:

            if time_checker(instance.updated_at, minute=10):
                instance.login_attempt = 0
                instance.save()
                pass
            else:
                return Response({'message': 'You have exceeded the maximum number of unsuccessful attempts. '
                                'Please try again after 10 minutes.'}, status=status.HTTP_403_FORBIDDEN)

        serializer_class = LoginSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            if instance.check_password(serializer.validated_data['password']):
                instance.login_attempt = 0
                instance.save()
                data = get_tokens_for_user(instance)
                data['last_login_time'] = instance.last_login
                data['detail'] = 'Login successful'
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                instance.login_attempt += 1
                instance.save()
                return Response({'message':'Invalid phone number or password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class LogoutViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        if 'refresh' not in request.data:
            return Response({'message': 'Token is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_202_ACCEPTED)
        except (TokenError, TokenBackendError):
            return Response({'message': 'Token is already blacklisted'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

@extend_schema(tags=['Reset Password'])
class ResetPasswordViewSet(ModelViewSet):
    model_class = UserModel
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        confirm_password = request.data.get('confirm_password', None)


        if not old_password or not new_password or not confirm_password:
            return Response({'message': 'Above information is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not new_password == confirm_password:
             return Response({'message': 'New password and confirm password must be same'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = self.model_class.objects.filter(id=request.user.id).first()

        if not instance:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = ResetPasswordSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            if instance.check_password(serializer.validated_data['old_password']):
                try:
                    validate_password(new_password)
                    instance.set_password(new_password)
                    instance.save()
                except ValidationError:
                    return Response({'message': 'Given password is too weak.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if not request.data['refresh']:
                return Response({'message': 'Token is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                token = RefreshToken(request.data['refresh'])
                token.blacklist()
                subject = 'Central Mart'
                message = 'Password reset was successful!'
                send_email(None, subject, message, request.user.id)
                return Response({'message': 'Password reset was successful. Please login again.'}, status=status.HTTP_202_ACCEPTED)
            except (TokenError, TokenBackendError):
                return Response({'message': 'Token is already blacklisted'}, status=status.HTTP_406_NOT_ACCEPTABLE)     
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@extend_schema(tags=['Forget Password'])
class ForgetPasswordViewSet(ModelViewSet):
    model_class = UserModel
    permission_classes = []
    serializer_class = ResetForgetPasswordSerializer

    def get_serializer_class(self):
        if self.action =='get_forget_password_mail':
            return ForgetPasswordSerializer
        else:
            return self.serializer_class

    def get_forget_password_mail(self, request, *args, **kwargs):
        email_id = request.data.get('email', None)
        if not email_id:
            return Response({'message': 'Email is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user_instance = self.model_class.objects.filter(email=request.data['email']).first()
            if not user_instance:
                return Response({"message": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Generate token and uid
        uid = urlsafe_base64_encode(force_bytes(user_instance.pk))
        token = default_token_generator.make_token(user_instance)
        print(user_instance)

        # Prepare email
        subject = "Central Mart: Password Reset Link"
        message = (
                "You requested a password reset. Please use the link below to reset your password: "
                f"http://127.0.0.1:8000/authentication/confirm-password/{uid}/{token}/. "
                "If you did not request this, please ignore this email."
            )
        send_email(None, subject, message, request.user.id)
        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
    

    def create_new_password(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user_instance = self.model_class.objects.filter(pk=uid).first()
        except (TypeError, ValueError, OverflowError, self.model_class.DoesNotExist):
            return Response({"message": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user_instance, token):
            password = request.data.get('password')
            if not password:
                return Response({"message": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    validate_password(password)
                    user_instance.set_password(password)
                    user_instance.save()
                except ValidationError:
                    return Response({'message': 'Given password is too weak.'}, status=status.HTTP_400_BAD_REQUEST)
                subject = 'Central Mart'
                message = 'Password reset was successful!'
                send_email(None, subject, message, request.user.id)
                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

   