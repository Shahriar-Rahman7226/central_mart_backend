from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.product_management.views.views import *

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubCategoryViewSet, basename='subcategory')
router.register('product', ProductViewSet, basename='product')
urlpatterns = [
                  path(r'', include(router.urls)),
              ]