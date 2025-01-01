from django.db import models

from abstract.base_model import CustomModel
from apps.address.models import AddressModel, HubModel
from external.choice_tuple import PaymentMethodType, VoucherType, OrderStatus
from apps.product_management.models import ProductModel
from apps.users.models import UserModel


class CartModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='cart_user', on_delete=models.CASCADE, blank=True, null=True)
    hub = models.ForeignKey(HubModel,  related_name='cart_hub', on_delete=models.CASCADE, blank=True, null=True)
    cart_status = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''} -- {self.hub.name if self.hub else ''} -- {self.cart_status if self.cart_status else 'No'}"

    class Meta:
        db_table = 'cart_models'
        ordering = ['-created_at']

class CartItemModel(CustomModel):
    cart = models.ForeignKey(CartModel, related_name='cart_item_cart', on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(ProductModel, related_name='cart_item_item', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    previous_quantity = models.PositiveIntegerField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True, help_text="Total cost for each item")
    weight = models.FloatField(blank=True, null=True, help_text="Total weight for each item")

    def __str__(self):
        return f"{self.item.title if self.item else ''}"

    class Meta:
        db_table = 'cart_item_models'
        ordering = ['-created_at']


class VoucherModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    minimum_amount = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=PaymentMethodType, default='CASH', blank=True, null=True)
    voucher_type = models.CharField(max_length=50, blank=True, null=True, choices=VoucherType)
    item = models.ForeignKey(ProductModel, related_name='voucher_item', on_delete=models.CASCADE, blank=True, null=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title if self.title else ''} -- {self.voucher_type if self.voucher_type else ''}"

    REQUIRED_FIELDS = ["amount"]
    class Meta:
        db_table = 'voucher_models'
        ordering = ['-created_at']


class OrderPaymentModel(CustomModel):
    order_id = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(UserModel, related_name='order_payment_user', on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(AddressModel, related_name='order_payment_address', on_delete=models.CASCADE, blank=True, null=True)
    cart = models.CharField(max_length=100, blank=True, null=True)
    hub = models.ForeignKey(HubModel, related_name='order_payment_hub', on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=PaymentMethodType, default='CASH', blank=True, null=True)
    sub_total = models.FloatField(blank=True, null=True)
    total_weight = models.FloatField(blank=True, null=True, help_text="Total weight of the order (in grams)")
    ask_delivery_fee = models.FloatField(blank=True, null=True)
    actual_delivery_fee = models.FloatField(blank=True, null=True)
    delivery_profit =  models.FloatField(blank=True, null=True)
    voucher = models.ForeignKey(VoucherModel, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    delivery_duration = models.TextField(blank=True, null=True)
    delivery_tracker = models.URLField(blank=True, null=True)
    delivery_status = models.TextField(max_length=100, blank=True, null=True, help_text="Delivery status (for customers)")
    order_status = models.CharField(max_length=100, blank=True, null=True, choices=OrderStatus, help_text="Order status (for admin)")
    reason = models.TextField(blank=True, null=True)
    # alter_status = models.BooleanField(blank=True, null=True, default=True)
    voucher_amount = models.FloatField(blank=True, null=True, default=0)
    order_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''} -- {self.hub.name if self.hub else ''} -- {self.order_id if self.order_id else ''} -- {self.order_status if self.order_status else ''}"

    class Meta:
        db_table = 'order_payment_models'
        ordering = ['-created_at']

    
class OrderReviewModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='order_review_user', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(OrderPaymentModel, related_name='order_review_order', on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    review_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.name if self.user else ''} -- {self.rating if self.rating else ''}"

    class Meta:
        db_table = 'order_review_models'
        ordering = ['-created_at']
    

