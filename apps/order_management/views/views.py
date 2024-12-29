
from django.db.models import Sum
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from external.choice_tuple import WeightUnit
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.order_management.serializers.serializers import *
from external.helper_functions import *
from apps.product_management.serializers.serializers import ProductCreateSerializer
from external.time_checker import time_frame_validator
from external.send_message import send_email, send_sms
from external.permission_decorator import allowed_users
from rest_framework import status
from external.query_helper import get_query_data
from django.utils import timezone
from datetime import timedelta
from apps.address.models import HubModel
from apps.address.serializers.serializers import UserHubSerializer

@extend_schema(tags=['Cart'])
class CartViewSet(ModelViewSet):
    model_class = CartModel
    serializer_class = CartListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action=='create':
            return CartCreateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Cart",
                value={
                    "hub": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['CUSTOMER'])
    def create(self, request, *args, **kwargs):
        expired_carts = self.queryset.filter(cart_status=False)
        expired_carts.delete()
            
        request.data['user'] = request.user.id
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Cart created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid cart'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Cart Item'])
class CartItemViewSet(ModelViewSet):
    model_class = CartItemModel
    serializer_class = CartItemListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CartItemCreateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Add Item",
                value={
                    "item": "string",
                    "quantity": 0,
                    "cart": "string",
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        data = request.data
       
        cart_instance = CartModel.objects.filter(id=data['cart']).first()
        if not cart_instance:
            return Response({'message': 'Invalid cart'}, status=status.HTTP_400_BAD_REQUEST)

        product_instance = ProductModel.objects.filter(id=data['item'], hub=cart_instance.hub).first()
        if not product_instance:
            return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)
        
        if product_instance.stock_status == 'STOCK_OUT':
            return Response({'message': 'Product out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        if data['quantity'] > product_instance.stock_level:
            return Response({'message': 'Sufficient quantity of product not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['cost'] = calc_product_cost(data['quantity'], product_instance.offered_price)
        data['weight'] = calc_product_weight(product_instance.weight, product_instance.weight_unit, data['quantity'])
        data['previous_quantity'] = data['quantity']

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            cart_item_obj = serializer.save()
            if request.user.user_role in ['ADMIN', 'MANAGER']:
                update_stock_status(cart_item_obj)
            return Response({'message': 'Item added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        examples=[
            OpenApiExample(
                "Update Item Quantity",
                value={
                    "quantity": 0,
                },
                request_only=True,
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.queryset.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid cart item'}, status=status.HTTP_400_BAD_REQUEST)
        if data['quantity'] == 0:
            if request.user.user_role in ['ADMIN', 'MANAGER']:
                    instance.previous_quantity = instance.quantity
                    update_stock_status(instance, True, True)
            instance.delete()
            return Response({'message': 'Product successfully removed from the cart'}, status=status.HTTP_200_OK)

        if instance:
            product_instance = ProductModel.objects.filter(id=instance.item, hub=instance.cart.hub).first()
            if not product_instance:
                return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)
            
            if product_instance.stock_status == 'STOCK_OUT':
                return Response({'message': 'Product out of stock'}, status=status.HTTP_400_BAD_REQUEST)
            if data['quantity'] > product_instance.stock_level:
                return Response({'message': 'Sufficient quantity of product not available'}, status=status.HTTP_400_BAD_REQUEST)
                
            data['cost'] = calc_product_cost(data['quantity'], product_instance.offered_price)
            data['weight'] = calc_product_weight(product_instance.weight, product_instance.weight_unit, data['quantity'])
            data['previous_quantity'] = instance.quantity

            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=instance, data=data)
            if serializer.is_valid(raise_exception=True):
                cart_item_obj=serializer.save()
                if request.user.user_role in ['ADMIN', 'MANAGER']:
                    update_stock_status(cart_item_obj, True)
                return Response({'message': 'Item quantity updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'cart', "description": 'Filter by cart'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        params = request.query_params
        if not params:
            return Response({'message': 'Cart id is required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset=get_query_data(params, queryset)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@extend_schema(tags=['Voucher'])
class VoucherViewSet(ModelViewSet):
    model_class = VoucherModel
    serializer_class = VoucherListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return VoucherCreateSerializer
        return self.serializer_class
    
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        data = request.data
        if data['start_date'] or data['expiry_date']:
            if data['start_date'] > data['expiry_date']:
                return Response({'messaage': 'Voucher expiry date must be greater or equal than start date'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Voucher created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        data=request.data
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Voucher does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        if data['start_date'] or data['expiry_date']:
            if data['start_date'] > data['expiry_date']:
                return Response({'message': 'Voucher expiry date must be greater or equal than start date'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Voucher updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'expiry_date', "description": 'Filter by expiry_date'},
        {"name": 'is_active', "description": 'Filter by is_active'},
        {"name": 'payment_method', "description": 'Filter by payment_method'},
        {"name": 'product_id', "description": 'Filter by product id'},
        {"name": 'voucher_type', "description": 'Filter by voucher_type'},
        {"name": 'is_free', "description": 'Filter by is_free'},
    ]))
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def list(self, request, *args, **kwargs):
        expired_vouchers = self.queryset.filter(expiry_date__lte=timezone.now())
        expired_vouchers.delete()

        queryset = self.queryset
        params = request.query_params

        queryset=get_query_data(params, queryset)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['CUSTOMER'])
    def get_voucher_list(self, request, *args, **kwargs):
        expired_vouchers = self.queryset.filter(expiry_date__lte=timezone.now())
        expired_vouchers.delete()

        queryset=self.queryset
        if request.user.user_role == 'CUSTOMER':
            queryset = get_vouchers(self.request.user.order_count, queryset)
        else:
            return Response({'message':'You donot have the permission to access this page'}, status=status.HTTP_403_FORBIDDEN)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data + '\n Voucher will be disabled if the product or minimum quantity is changed', status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid voucher'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)    


@extend_schema(tags=['Order Payment'])
class OrderPaymentViewSet(ModelViewSet):
    model_class = OrderPaymentModel
    serializer_class = OrderPaymentListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'update_by_customer']:
            return OrderPaymentCreateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Order Payment",
                value={
                    "user": "string",
                    "address": "string",
                    "payment_method": "string",
                    "voucher": "string",
                    "cart": "string",
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['CUSTOMER'])
    def create(self, request, *args, **kwargs):
        data = request.data

        cart_instance = CartModel.objects.filter(id=data['cart'], status=False).first()
        if not cart_instance:
            return Response({'message': 'Invalid cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart_queryset = CartItemModel.objects.filter(cart=cart_instance)
        data['hub'] = cart_instance.hub
       
        # sub total calculation
        data['sub_total'] = cart_queryset.aggregate(total_cost=Sum('cost'))['total_cost']

        # total weight calculation
        data['total_weight'] = cart_queryset.aggregate(total_weight=Sum('weight'))['total_cost']

        # voucher validation
        if data['voucher']:
            voucher_flag=False
            voucher_instance = VoucherModel.objects.filter(id=data['vouhcer']).first()
            if voucher_instance:
                if voucher_instance.minimum_amount:
                    if data['sub_total']>=voucher_instance.minimum_amount:
                        voucher_flag=True
                if voucher_instance.item:
                    voucher_flag=False
                    for data in cart_queryset:
                        if voucher_instance.item==data.id:
                            voucher_flag=True
                            break
                if voucher_instance.payment_method:
                    voucher_flag=False
                    if data['payment']==voucher_instance.payment_method:
                        voucher_flag=True  
            if not voucher_flag or not voucher_instance:
                return Response({'message': 'Voucher is not available'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                 if voucher_instance.is_free:
                    data['voucher_amount'] = - 1 
                 elif voucher_instance.amount: 
                    data['voucher_amount'] = data['voucher'].amount
                 elif voucher_instance.percentage:
                    data['voucher_amount'] = data['sub_total'] * voucher_instance.percentage

        # delivery fee calculation
        data['ask_delivery_fee'] = calc_delivery_fee(data['total_weight'], data['hub'], data['address'].district, data['voucher_amount'])
        data['actual_delivery_fee'] = data['ask_delivery_fee']*(90/100)
        data['delivery_profit'] = data['ask_delivery_fee'] - data['actual_delivery_fee']        # 10% profit for now

        data['total'] = data['sub_total'] - data['delivery_fee'] - (data['voucher_amount'] if data['voucher_amount'] != -1 else 0)

        data['delivery_duration'] = get_delivery_duration(data['hub'])
        data['order_status'] = OrderStatus[0][0]
        data['delivery_status'] = get_delivery_status(data['order_status'])

        response_data = {
            'delivery_duration': data['delivery_duration'],
            'delivery_status': data['delivery_status'],
            'message': "You can cancel or update your order address within the city, or contact us for changes within the next hour."
        }
        

        order_history = []
        for item in cart_queryset:
            order_detail = f"Item: {item.item.title}, Quantity: {item.quantity}, Price: {item.cost}"
            order_history.append(order_detail)

        data['order_details'] = "\n".join(order_history)

        order_details += f"\n\nSubtotal: {data['subtotal']}"
        order_details += f"\nDelivery Fee: {data['delivery_fee']}"
        order_details += f"\nVoucher Discount: {data['voucher_amount'] if data['voucher_amount'] != -1 else 0}"
        order_details += f"\nTotal: {data['total']}"

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_obj = serializer.save()
            update_stock_status(cart_queryset)
            data = {
                'user': cart_instance.user,
                'hub': cart_instance.hub,
                'cart_status': True,
            }
            cart_serializer = CartCreateSerializer(instance=cart_instance, data=data)
            if cart_serializer.is_valid(raise_exception=True):
                cart_serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            subject = 'Central Mart'
            message = (f"Order id: {order_obj.id}\n {order_obj.delivery_status}\n {order_obj.delivery_duration}\n"
                       f"You can cancel or update your order address within the city, or contact us for changes within the next hour.\n"
                       f"{order_obj.order_details}")
            send_email(None, subject, message, request.user.id)
            # send_sms()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        examples=[
            OpenApiExample(
                "Update Order",
                value={
                    "address": "string",
                    "order_status": "string",
                    "reason": "string",
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['CUSTOMER'])
    def update_by_customer(self, request, *args, **kwargs):
        data = request.data
        order_instance = OrderPaymentModel.objects.filter(id=kwargs['id']).first()
        if not order_instance:
            return Response({'message': 'Invalid order'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()
    
        one_hour_ago = current_time - timedelta(hours=1)
    
        if order_instance.created_at < one_hour_ago:
            return Response({'message': 'Sorry, You cannot make any changed to the order now'}, status=status.HTTP_200_OK)
        
        if data['order_status']:
            if data['order_status']=='CANCELLED':
                if not data['reason']:
                    return Response({'message': 'Please state a reason for your cancellation'}, status=status.HTTP_200_OK)
                else:
                    message='Your order was cancelled successfully'
                    cart_instance = CartModel.objects.filter(id=order_instance.cart).first()
                    cart_queryset = CartItemModel.objects.filter(cart=cart_instance)
                    update_stock_status(cart_queryset, False, False, True)
                    cart_instance.delete()
            else:
                return Response({'message': 'Invalid order status'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
        if data['address']:
            address_instance = AddressModel.objects.filter(id=data['addrress'], user=order_instance.user).first()
            if not address_instance.district == order_instance.address.district:
                return Response({'message': 'Address needs to inside the city'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                message='Your order address was updated successfully'
            
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=order_instance, data=data)
        if serializer.is_valid(raise_exception=True): 
                order_obj=serializer.save()
                subject = 'Central Mart'
                message = f"Order id: {order_obj.id}\n {message}"
                send_email(None, subject, message, request.user.id)
                # send_sms()
                return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
            
    @extend_schema(
        examples=[
            OpenApiExample(
                "Update Order Payment",
                value={
                    "discount": 0.0,
                    "hub": "string",
                    "order_status": "string",
                    "delivery_tracker": "string",
                    "cart": "string",
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        data = request.data

        order_instance = OrderPaymentModel.objects.filter(id=kwargs['id']).first()
        if not order_instance:
            return Response({'message': 'Invalid order'}, status=status.HTTP_400_BAD_REQUEST)
        
        if data['cart']:
            cart_instance = CartModel.objects.filter(id=order_instance.cart, cart_status=True).first()
            if not cart_instance:                                                                                                                                                                                                                                                                                                                                                                                                                                  
                return Response({'message': 'Invalid cart'}, status=status.HTTP_400_BAD_REQUEST)
            cart_queryset = CartItemModel.objects.filter(cart=cart_instance)
            
            # sub total calculation
            data['sub_total'] = cart_queryset.aggregate(total_cost=Sum('cost'))['total_cost']
            # total weight calculation
            data['total_weight'] = cart_queryset.aggregate(total_weight=Sum('weight'))['total_cost']

            # voucher validation
            if order_instance.voucher:
                voucher_flag=False
                voucher_instance = VoucherModel.objects.filter(id=data['vouhcer']).first()
                if voucher_instance:
                    if voucher_instance.minimum_amount:
                        if data['sub_total']>=voucher_instance.minimum_amount:
                            voucher_flag=True
                    if voucher_instance.item:
                        voucher_flag=False
                        for data in cart_queryset:
                            if voucher_instance.item==data.id:
                                voucher_flag=True
                                break
                if not voucher_flag or not voucher_instance:
                    data['voucher_amount'] = 0
                else:
                    if voucher_instance.is_free:
                        data['voucher_amount'] = - 1 
                    data['sub_total'] = data['sub_total'] - (order_instance.voucher_amount if order_instance.voucher_amount != -1 else 0)
                
            # delivery fee calculation
            data['ask_delivery_fee'] = calc_delivery_fee(data['total_weight'], data['hub'], order_instance.address.district, data['voucher_amount'])
            data['actual_delivery_fee'] = data['ask_delivery_fee']*(90/100)
            data['delivery_profit'] = data['ask_delivery_fee'] - data['actual_delivery_fee']        # 10% profit for now
            data['total'] = data['sub_total'] - data['delivery_fee']
        
        if data['discount']:
                data['total'] = data['total'] - data['discount']
        
        if data['order_status']:
            data['delivery_status'] = get_delivery_status(data['order_status'])

        if data['order_status']=='DELIVERED':
            update_user_order_count(data['user'])
            order_instance.cart.delete()

        response_data = {
            'delivery_status': data['delivery_status'],
            'delivery_tracker': data['delivery_tracker'] if data['delivery_tracker'] else ''
        }

        order_history = []
        for item in cart_queryset:
            order_detail = f"Item: {item.item.title}, Quantity: {item.quantity}, Price: {item.cost}"
            order_history.append(order_detail)

        data['order_details'] = "\n".join(order_history)

        order_details += f"\n\nSubtotal: {data['subtotal']}"
        order_details += f"\nDelivery Fee: {data['delivery_fee']}"
        order_details += f"\nVoucher Discount: {data['voucher_amount'] if data['voucher_amount'] != -1 else 0}"
        order_details += f"\nTotal: {data['total']}"

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=order_instance, data=data)
        if serializer.is_valid(raise_exception=True): 
                order_obj=serializer.save()
                if data['cart']:
                    update_stock_status(cart_queryset)
                subject = 'Central Mart'
                message = f"Order id: {order_obj.id}\n {order_obj.delivery_status}\n {order_obj.order_details}"
                message = f"Order id: {order_obj.id}\n {order_obj.delivery_status}"
                send_email(order_obj.id, subject, message, None)
                # send_sms()
                return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'time_frame', "description": 'Filter by time_frame (e.g: 6months)'},
        {"name": 'user', "description": 'Filter by user Id'},
        {"name": 'hub', "description": 'Filter by hub Id)'},
        {"name": 'payment_method', "description": 'Filter by payment method'},
        {"name": 'order_status', "description": 'Filter by order status'},
    ]))
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        if 'time_frame' in request.query_params:
            query_time = time_frame_validator(request.query_params.get('time_frame'))
            if query_time:
                queryset = queryset.filter(created_at__gte=query_time)
        if 'user' in request.query_params:
            queryset = queryset.filter(user=request.query_params.get('user'))
        if 'hub' in request.query_params:
            queryset = queryset.filter(hub=request.query_params.get('hub'))
        if 'payment_method' in request.query_params:
            queryset = queryset.filter(payment_method=request.query_params.get('payment_method'))
        if 'order_status' in request.query_params:
            queryset = queryset.filter(order_status=request.query_params.get('order_status'))
 
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid order'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @allowed_users(allowed_roles=['CUSTOMER'])
    def get_order_history(self, request, *args, **kwargs):
        queryset = self.queryset(user=request.user.id)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            order_details = [order.order_details for order in page]
            return self.get_paginated_response(order_details)
        order_details = [order.order_details for order in queryset]
        return Response(order_details, status=status.HTTP_200_OK)
    
    @extend_schema(parameters=set_query_params('list', [
        {"name": 'product_id', "description": 'Get related products'},
    ]))
    @allowed_users(allowed_roles=['CUSTOMER'])
    def get_related_items(self, request, *args, **kwargs):
        if not 'product_id' in request.query_params:
            return Response({'message': 'Product id is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = ProductModel.objects.all()

        product_instance =queryset.filter(id=request.query_params.get('product_id')).first()
        if not product_instance:
            return Response({'message': 'Invalid product id'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = queryset.filter(subcategory=product_instance.subcategory, hub=product_instance.hub).exclude(id=product_instance.id) 
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    
    
