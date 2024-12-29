from django.apps import apps

from django.contrib import admin

from apps.users.models import *

# Register your models here.

from django.apps import apps
from django.contrib import admin


class UserModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'phone_number')


admin.site.register(UserModel, UserModelAdmin)