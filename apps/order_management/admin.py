from django.contrib import admin
from apps.order_management.models import *

# Register your models here.
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(VoucherModel)
admin.site.register(OrderPaymentModel)
admin.site.register(OrderReviewModel)