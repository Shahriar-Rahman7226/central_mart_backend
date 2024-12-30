from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views.views import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('user-registration', UserResgistrationViewSet, basename='user_registration')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('create-admin/', UserResgistrationViewSet.as_view({'post': 'create_admin'})),
                  path('create-manager/', UserResgistrationViewSet.as_view({'post': 'create_manager'})),
                  path('create-customer/', CustomerResgistrationViewSet.as_view({'post': 'create_customer'})),
                  path('get-customer-list/', UserResgistrationViewSet.as_view({'get': 'get_customer_list'})),
              ] 