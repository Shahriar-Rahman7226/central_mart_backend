from external.choice_tuple import VoucherType
from apps.product_management.models import ProductModel
from django.forms.models import model_to_dict
from apps.order_management.models import VoucherModel
from apps.product_management.serializers.serializers import ProductCreateSerializer
from apps.users.serializers.serializers import UserUpdateSerializer
from apps.address.models import HubModel
from rest_framework.response import Response
from rest_framework import status

#FOR PRODUCT MANAGEMENT APP#
def calc_gross_profit(sp, cp):
    gross_profit = sp-cp
    return gross_profit

def calc_profit_margin(gp, cp):
    profit_margin =  (gp/cp)*100
    return profit_margin


#FOR ORDER MANAGEMENT APP#
def calc_product_cost(quantity, price):
    cost = quantity*price
    return cost

def calc_product_weight(weight, unit, quantity):
    if unit == 'KILOGRAM' or unit == 'LITRE':
        weight = weight*1000
    weight = weight*quantity
    # print(unit)
    return weight

    
def get_vouchers(order_count, queryset=[]):
    if not queryset:
        queryset = VoucherModel.objects.all()
    if order_count == 0:
        vouchers = queryset.filter(voucher_type=VoucherType[0][0], is_active=True)
    elif 0 < order_count <= 10:
        vouchers = queryset.filter(voucher_type=VoucherType[0][1], is_active=True)
    elif order_count > 10:
        vouchers = queryset.filter(voucher_type=VoucherType[0][2], is_active=True)
    
    if order_count > 0:
        general_vouchers = queryset.filter(voucher_type=VoucherType[0][3], is_active=True)
        vouchers = vouchers | general_vouchers if vouchers.exists() else general_vouchers # Union of the querysets

    return vouchers


def calc_delivery_fee(weight, hub, district, voucher):
    fee = 0
    inside_city = False
    # print(voucher)

    if voucher == -1:
        return fee
    hub_instance = HubModel.objects.filter(id=hub, district=district).first()
    # print(hub_instance.name)

    if  hub_instance:
        inside_city = True

    if inside_city:
        if 400 < weight <= 800:
            fee = 80
        elif 800 < weight <= 1600:
            fee = 100
        elif weight > 1600:
            fee = 100 + (((weight - 1600) / 1000) * 20)
        else:
            fee = 70
    else:
        if 400 < weight <= 800:
            fee = 150.0
        elif 800 < weight <= 1600:
            fee = 190.0
        elif weight > 1600:
            fee = 190.0 + (((weight - 1600) / 1000) * 30)
        else:
            fee = 130
    return fee


def get_delivery_duration(hub):
    inside_city = False
    hub_instance = HubModel.objects.filter(name=hub).first()

    if  hub_instance:
        inside_city = True
    
    if inside_city:
        delivery_duration = 'You will receive your order within 24 hours'
    else:
        delivery_duration = 'You will receive your order within 3 days'
    return delivery_duration


def get_delivery_status(order_status):

    if order_status == 'PROCESSING':
        delivery_status_message = "Your order is being processed."
    elif order_status == 'CONFIRMED':
        delivery_status_message = "Your order has been confirmed."
    elif order_status == 'IN_TRANSIT':
        delivery_status_message = "Your order is on its way."
    elif order_status == 'DELIVERED':
        delivery_status_message = "Your order has been delivered."
    elif order_status == 'CANCELLED':
        delivery_status_message = "Your order has been cancelled."
    elif order_status == 'RETURNED':
        delivery_status_message = "Your order has been returned."
    return delivery_status_message

def update_stock_status(cart_queryset, cart_instance=None, admin_update=False, admin_delete=False, customer_delete=False):
    product_queryset = ProductModel.objects.all()
    if customer_delete==True:
         for item in cart_queryset:
            instance = product_queryset.filter(id=item.item.id).first()
            if instance:
                data = {
                            'stock_level': instance.stock_level + item.quantity,
                            'order_count': instance.order_count - 1,
                            'weight_unit': instance.weight_unit if instance.weight_unit else ''
                        } 
                serializer = ProductCreateSerializer(data=data, instance=instance)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST) 
    elif admin_delete==False:
        if cart_instance:
            instance = product_queryset.filter(id=cart_instance.item.id).first()
            if instance:
                data = {
                            'stock_level': instance.stock_level - (cart_instance.quantity if admin_update == False else cart_instance.quantity-cart_instance.previous_quantity),
                            'order_count': instance.order_count + (1 if admin_update == False else 0),
                            'weight_unit': instance.weight_unit if instance.weight_unit else ''
                        } 
                serializer = ProductCreateSerializer(data=data, instance=instance)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            for item in cart_queryset:
                instance = product_queryset.filter(id=item.item.id).first()
                if instance:
                    data = {
                                'stock_level': instance.stock_level - (item.quantity if admin_update == False else item.quantity-item.previous_quantity),
                                'order_count': instance.order_count + (1 if admin_update == False else 0),
                                'weight_unit': instance.weight_unit if instance.weight_unit else ''
                            } 
                    serializer = ProductCreateSerializer(data=data, instance=instance)
                    if serializer.is_valid(raise_exception=True):
                        obj = serializer.save()
                        print(obj)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        instance = product_queryset.filter(id=cart_instance.item.id).first()
        if instance:
            data = {
                        'stock_level': instance.stock_level + cart_instance.previous_quantity,
                        'order_count': instance.order_count - 1,
                        'weight_unit': instance.weight_unit if instance.weight_unit else ''
                    } 
            serializer = ProductCreateSerializer(data=data, instance=instance)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)


def update_user_order_count(user):
        data = {
                    'order_count': user.order_count +1
        }
        serializer = UserUpdateSerializer(data=data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

