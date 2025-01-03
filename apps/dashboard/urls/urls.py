from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.dashboard.views.views import *


router = DefaultRouter()
router.register('banner', BannerViewSet, basename='banner')

urlpatterns = [
                  path(r'', include(router.urls)),
              ] 