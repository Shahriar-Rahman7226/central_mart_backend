from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.address.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class DivisionCreateSerializer(ModelSerializer):
    class Meta:
        model = DivisionModel
        exclude = exclude_list + ['id']

class DivisionListSerializer(ModelSerializer):
    class Meta:
        model = DivisionModel
        exclude = exclude_list


class DistrictCreateSerializer(ModelSerializer):
    class Meta:
        model = DistrictModel
        exclude = exclude_list + ['id']


class DistrictListSerializer(ModelSerializer):
    division = serializers.SerializerMethodField()
    class Meta:
        model = DistrictModel
        exclude = exclude_list

    def get_division(self, obj):
        division = obj.division
        return DivisionListSerializer(division).data


class SubDistrictCreateSerializer(ModelSerializer):
    class Meta:
        model = SubDistrictModel
        exclude = exclude_list + ['id']


class SubDistrictListSerializer(ModelSerializer):
    district = serializers.SerializerMethodField()
    class Meta:
        model = SubDistrictModel
        exclude = exclude_list

    def get_district(self, obj):
        district = obj.district
        return DistrictListSerializer(district).data

class HubCreateSerializer(ModelSerializer):
    class Meta:
        model = HubModel
        exclude = exclude_list + ['id']

class HubListSerializer(ModelSerializer):
    class Meta:
        model = HubModel
        exclude = exclude_list

class AddressCreateSerializer(ModelSerializer):
    label = serializers.ChoiceField(choices=AddressLabelType)

    class Meta:
        model = AddressModel
        exclude = exclude_list + ['id']


class AddressListSerializer(ModelSerializer):
    sub_district = serializers.SerializerMethodField()
    class Meta:
        model = AddressModel
        exclude = exclude_list

    def get_sub_district(self, obj):
        sub_district = obj.sub_district
        return SubDistrictListSerializer(sub_district).data


class UserHubSerializer(ModelSerializer):
    class Meta:
        model = AddressModel
        exclude = exclude_list 