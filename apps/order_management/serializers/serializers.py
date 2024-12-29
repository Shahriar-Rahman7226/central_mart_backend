from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.order_management.models import *
from apps.users.serializers.serializers import UserListSerializer

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class CartCreateSerializer(ModelSerializer):
    class Meta:
        model = CartModel
        exclude = exclude_list 


class CartItemCreateSerializer(ModelSerializer):
    class Meta:
        model = CartItemModel
        exclude = exclude_list


class CartItemListSerializer(ModelSerializer):
    class Meta:
        model = CartItemModel
        exclude = exclude_list


class CartListSerializer(ModelSerializer):
    cart_item_cart = SerializerMethodField(read_only=True)
    user_info = SerializerMethodField(read_only=True, required=False)

    def get_user_info(self, obj):
        return UserListSerializer(obj.user).data

    def get_cart_item_cart(self, obj):
        cart_item_cart = obj.cart_item_cart.all()
        return CartItemListSerializer(cart_item_cart, many=True).data

    class Meta:
        model = CartModel
        exclude = exclude_list


class VoucherCreateSerializer(ModelSerializer):
    payment_method = serializers.ChoiceField(choices=PaymentMethodType)
    voucher_type = serializers.ChoiceField(choices=VoucherType)

    class Meta:
        model = VoucherModel
        exclude = exclude_list + ['id']


class VoucherListSerializer(ModelSerializer):
    class Meta:
        model = VoucherModel
        exclude = exclude_list


class OrderPaymentCreateSerializer(ModelSerializer):
    payment_method = serializers.ChoiceField(choices=PaymentMethodType)
    order_status = serializers.ChoiceField(choices=OrderStatus)

    class Meta:
        model = OrderPaymentModel
        exclude = exclude_list + ['id']


class OrderPaymentListSerializer(ModelSerializer):
    class Meta:
        model = OrderPaymentModel
        exclude = exclude_list

class OrderReviewSerializer(ModelSerializer):

    class Meta:
        model = OrderReviewModel
        exclude = exclude_list