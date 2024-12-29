from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.address.models import *
from apps.address.serializers.serializers import *
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from external.permission_decorator import allowed_users
from rest_framework import status
from external.query_helper import get_query_data
from external.choice_tuple import UserRole


@extend_schema(tags=['Division'])
class DivisionViewSet(ModelViewSet):
    model_class = DivisionModel
    serializer_class = DivisionListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DivisionCreateSerializer
        return self.serializer_class

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Division created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid division'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Division updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
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


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid division'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['District'])
class DistrictViewSet(ModelViewSet):
    model_class = DistrictModel
    serializer_class = DistrictListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DistrictCreateSerializer
        return self.serializer_class
    
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': "District created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid district'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'District updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'division', "description": 'Filter by division Id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
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


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid district'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Sub-District'])
class SubDistrictViewSet(ModelViewSet):
    model_class = SubDistrictModel
    serializer_class = SubDistrictListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SubDistrictCreateSerializer
        return self.serializer_class

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Sub-district created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid sub-district'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Sub-district updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'division', "description": 'Filter by division Id'},
        {"name": 'district', "description": 'Filter by district Id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
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

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid sub-district'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Hub'])
class HubViewSet(ModelViewSet):
    model_class = HubModel
    serializer_class = HubListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return HubCreateSerializer
        return self.serializer_class

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Hub created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid hub'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Hub updated successfully'}, status=status.HTTP_200_OK)
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
            return Response({'message': 'Hub does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Address'])
class AddressViewSet(ModelViewSet):
    model_class = AddressModel
    serializer_class = AddressListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AddressCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        data = request.data
        user_instance = UserModel.objects.filter(id=request.user.id)
        if not user_instance:
            return Response({'message': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['label'] = data['label'].upper()
        if not data['label'] == 'OTHER':
            data['label_name'] = data['label']
        else:
            data['label_name'] = data['label_name'].upper()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Address created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid address'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['label'] = data['label'].upper()
        if not data['label'] == 'OTHER':
            data['label_name'] = data['label']
        else:
            data['label_name'] = data['label_name'].upper()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Address updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @extend_schema(parameters=set_query_params('list', [
        {"name": 'user', "description": 'Filter by user Id'},
        {"name": 'division', "description": 'Filter by division Id'},
        {"name": 'district', "description": 'Filter by district Id'},
        {"name": 'sub-district', "description": 'Filter by sub-district Id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user__user_role='CUSTOMER')
        params = request.query_params
        if params:
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
            return Response({'message': 'Invalid address'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['CUSTOMER'])
    def get_address_list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user.id)

        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        