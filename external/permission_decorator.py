from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(self, request, *args, **kwargs):
            user_role = request.user.user_role
            print(user_role)
            if user_role in allowed_roles or request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            else:
                return Response({"message": "You do not have the permission to view this content."}, status=status.HTTP_403_FORBIDDEN)
        return wrapper_func
    return decorator