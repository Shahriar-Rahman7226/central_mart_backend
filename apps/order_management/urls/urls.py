from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.order_management.views.views import *

router = DefaultRouter()
router.register('shopping-cart', CartViewSet, basename='shopping_cart')
router.register('voucher', VoucherViewSet, basename='voucher')
router.register('order-request', OrderPaymentViewSet, basename='order_request')
urlpatterns = [
                  path(r'', include(router.urls)),
                  path('get-voucher-list/', VoucherViewSet.as_view({'get': 'get_voucher_list'})),
                  path('update-by-customer/', OrderPaymentViewSet.as_view({'put': 'update_by_customer'})),
                  path('get-order-history/', OrderPaymentViewSet.as_view({'get': 'get_order_history'})),
                  path('get-related-items/', OrderPaymentViewSet.as_view({'get': 'get_related_items'})),
              ]