from drf_spectacular.utils import extend_schema, OpenApiExample
from nested_multipart_parser import NestedParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.product_management.models import *
from apps.product_management.serializers.serializers import *
from django.db import transaction
from external.helper_functions import * 
from external.permission_decorator import allowed_users
from rest_framework import status
from external.choice_tuple import UserRole
from external.query_helper import get_query_data

@extend_schema(tags=['Category'])
class CategoryViewSet(ModelViewSet):
    model_class = CategoryModel
    serializer_class = CategoryListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CategoryCreateSerializer
        return self.serializer_class
    
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Category updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.queryset
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
            return Response({'message': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Sub-Category'])
class SubCategoryViewSet(ModelViewSet):
    model_class = SubCategoryModel
    serializer_class = SubCategoryListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SubCategoryCreateSerializer
        return self.serializer_class

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        category_instance = CategoryModel.objects.filter(id=request.data['category']).first()
        if not category_instance:
            return Response({'message': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Sub Category created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id'], category=request.data['category']).first()
        if not instance:
            return Response({'message': 'Invalid sub category'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Sub Category updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'catergory', "description": 'Filter by category Id'},
    ]))
    def list(self, request, *args, **kwargs):
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

  
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid sub category'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Product'])
class ProductViewSet(ModelViewSet):
    model_class = ProductModel
    serializer_class = ProductListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductCreateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Product",
                value={
                    "title": "string",
                    "description": "string",
                    "category": "string",
                    "subcategory": "string",
                    "tag": "string",
                    "hub": "string",
                    "weight": 0.0,
                    "weight_unit": "string",
                    "stock_status": "string",
                    "stock_level": 10,
                    "regular_price": 0.0,
                    "offered_price": 0.0,
                    "cost_price": 0.0,
                    "is_published": False,
                    "is_featured": False,
                    "featured_details": "string",
                    "promotion_tag": "string",
                    "product_images": [{
                        "image": "file"
                    }]
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        if "product_images" in data:
            parsed_data = NestedParser(data)
            parsed_data.is_valid()
            validate_data = parsed_data.validate_data
            product_images = validate_data.pop("product_images", None)

        category_instance = CategoryModel.objects.filter(id=data['category']).first()
        if not category_instance:
            return Response({'message': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)

        subcategory_instance = SubCategoryModel.objects.filter(id=data['subcategory']).first()
        if not subcategory_instance:
            return Response({'message': 'Invalid sub-category'}, status=status.HTTP_400_BAD_REQUEST)

        if not data['offered_price'] or data['offered_price']==0:
            data['offered_price'] = data['regular_price']
        data['gross_profit'] = calc_gross_profit(data['offered_price'], data['cost_price'])
        data['profit_margin'] = calc_profit_margin(data['gross_profit'], data['cost_price'])

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            product_obj = serializer.save()
            if 'product_images' in request.data:
                if len(product_images) > 5:
                    return Response({'message': 'You can only upload up to 5 images.'}, status=status.HTTP_400_BAD_REQUEST)
                
                for item in product_images:
                    data = {
                        'product': product_obj.id,
                        'image': item.get('image', None)
                    }
                    image_serializer = ProductImageSerializer(data=data)
                    if image_serializer.is_valid(raise_exception=True):
                        image_serializer.save()
                    return Response(image_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        examples=[
            OpenApiExample(
                "Update Product",
                value={
                    "title": "string",
                    "description": "string",
                    "category ": "string",
                    "subcategory": "string",
                    "tag": "string",
                    "hub": "string",
                    "weight": 0.0,
                    "weight_unit": "string",
                    "stock_status": "string",
                    "stock_level": 10,
                    "regular_price": 0.0,
                    "offered_price": 0.0,
                    "cost_price": 0.0,
                    "is_published": False,
                    "is_featured": False,
                    "featured_details": "string",
                    "promotion_tag": "string",
                    "product_images": [{
                        'id': 0,
                        'image': 'file'
                    }]
                },
                request_only=True,
            )
        ]
    )
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        data = request.data
        if 'product_images' in request.data:
            parsed_data = NestedParser(data)
            parsed_data.is_valid()
            validate_data = parsed_data.validate_data
            product_images = validate_data.pop('product_images', None)

        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)

        if not data['offered_price']:
            data['offered_price'] = data['selling_price']
        data['gross_profit'] = calc_gross_profit(data['offered_price'], data['cost_price'])
        data['profit_margin'] = calc_profit_margin(data['gross_profit'], data['offered_price'])

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=data)
        if serializer.is_valid(raise_exception=True):
            product_obj = serializer.save()
            if 'product_images' in request.data:
                image_queryset = ProductImageModel.objects.filter(product=kwargs['id'])
                current_image_count = image_queryset.count()
                for item in product_images:
                    image_id = item.get('id', None)
                    data = {
                        'product': product_obj.id,
                        'image': item.get('image', None)
                    }
                    if image_id:
                        image_instance = ProductImageModel.objects.filter(id=image_id, product=product_obj.id)
                        if not image_instance:
                            return Response({'message': 'Invalid image id'}, status=status.HTTP_400_BAD_REQUEST)
                        image_serializer = ProductImageSerializer(instance=image_instance, data=data, partial=True)
                    elif(current_image_count<5):
                        image_serializer = ProductImageSerializer(data=data)
                    else:
                        return Response({'message': 'You can only upload up to 5 images.'}, status=status.HTTP_400_BAD_REQUEST)
                    if image_serializer.is_valid(raise_exception=True):
                        image_serializer.save()
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'category', "description": 'Filter by category Id'},
        {"name": 'subcategory', "description": 'Filter by sub-category Id'},
        {"name": 'hub', "description": 'Filter by hub Id'},
        {"name": 'is_featured', "description": 'Filter by featured status'},
        {"name": 'is_published', "description": 'Filter by published status'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        params = request.query_params
        if 'hub' not in params:
            params['hub'] = 'DHAKA'

        queryset=get_query_data(params, queryset)
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
            return Response({'message': 'Invalid product'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)