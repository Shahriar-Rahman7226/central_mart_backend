from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.product_management.models import *
from core import settings

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = exclude_list + ['id']


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = exclude_list


class SubCategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = SubCategoryModel
        exclude = exclude_list + ['id']


class SubCategoryListSerializer(ModelSerializer):
    class Meta:
        model = SubCategoryModel
        exclude = exclude_list


class ProductCreateSerializer(ModelSerializer):
    weight_unit = serializers.ChoiceField(choices=WeightUnit)
    # stock_status = serializers.ChoiceField(choices=StockStatus)

    class Meta:
        model = ProductModel
        exclude = exclude_list + ['id']

class ProductImageSerializer(ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ProductImageModel
        exclude = exclude_list

    def get_image(self, obj):
        # Check if the image exists and construct the full URL
        if obj.image:
            return f"{settings.SITE_URL}{obj.image.url}"  # Using SITE_URL to get the full URL
        return None  # Return None if there's no image

class ProductListSerializer(ModelSerializer):
    product_image = serializers.SerializerMethodField()
    class Meta:
        model = ProductModel
        exclude = exclude_list

    def get_product_image(self, obj):
        product_image = obj.product_image.all()
        return ProductImageSerializer(product_image, many=True).data


