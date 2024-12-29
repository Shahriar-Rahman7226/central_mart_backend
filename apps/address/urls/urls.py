from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.address.views.views import *


router = DefaultRouter()
router.register('division', DivisionViewSet, basename='division')
router.register('district', DistrictViewSet, basename='district')
router.register('thana', SubDistrictViewSet, basename='thana')
router.register('hub', HubViewSet, basename='hub')
router.register('address', AddressViewSet, basename='address')


urlpatterns = [
                  path(r'', include(router.urls)),
                  path('get-address-list/', AddressViewSet.as_view({'get': 'get_address_list'})),
              ] 