from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.product_management.models import *

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


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = exclude_list


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImageModel
        exclude = exclude_list