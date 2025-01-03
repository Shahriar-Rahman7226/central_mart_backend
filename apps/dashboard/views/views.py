from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.dashboard.models import *
from apps.dashboard.serializers.serializers import *
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from external.permission_decorator import allowed_users
from rest_framework import status


@extend_schema(tags=['Banner Image'])
class BannerViewSet(ModelViewSet):
    model_class = BannerModel
    serializer_class = BannerSerializer
    queryset = model_class.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @allowed_users(allowed_roles=['ADMIN', 'MANAGER'])
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid banner image'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Banner image updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        for banner in queryset:
            print(f"Image URL: {banner.image.url}")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid banner image'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)