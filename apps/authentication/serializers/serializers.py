from rest_framework.serializers import *
from apps.users.models import UserModel

class LoginSerializer(Serializer):
    phone_number = CharField(max_length=20, allow_blank=False, allow_null=False)
    password = CharField(max_length=128, allow_blank=False, allow_null=False)


class LogoutSerializer(Serializer):
    refresh = CharField(max_length=128, allow_blank=False, allow_null=False)


class ResetPasswordSerializer(Serializer):
    old_password = CharField(max_length=128, write_only=True)
    new_password = CharField(max_length=128, write_only=True)
    confirm_password = CharField(max_length=128, write_only=True)
    refresh = CharField(max_length=279, allow_blank=False, allow_null=False)


class ForgetPasswordSerializer(Serializer):
    email = EmailField(required=True)

class ResetForgetPasswordSerializer(Serializer):
     password = CharField(max_length=128, allow_blank=False, allow_null=False)