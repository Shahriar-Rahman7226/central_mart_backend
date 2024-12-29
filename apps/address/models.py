from django.db import models

from abstract.base_model import CustomModel
from external.choice_tuple import AddressLabelType
from apps.users.models import UserModel


# Create your models here.
class DivisionModel(CustomModel):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name if self.name else ''}"

    class Meta:
        db_table = 'division_models'
        ordering = ["-created_at"]


class DistrictModel(CustomModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    division = models.ForeignKey(DivisionModel, related_name='district_division', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name if self.name else ''} -- {self.division.name if self.division else ''}"

    class Meta:
        db_table = 'district_models'
        ordering = ["-created_at"]


class SubDistrictModel(CustomModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    division = models.ForeignKey(DivisionModel, related_name='sub_district_division', blank=True, null=True, on_delete=models.CASCADE)
    district = models.ForeignKey(DistrictModel, related_name='sub_district_district', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name if self.name else ''} -- {self.district.name if self.division else ''} -- {self.division.name if self.division else ''}"

   
    class Meta:
        db_table = 'sub_district_models'
        ordering = ["-created_at"]
        verbose_name='Sub-District model'

class HubModel(CustomModel):
    district = models.ForeignKey(DistrictModel, related_name='hub_district', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name if self.name else ''} -- {self.district.name if self.district else ''}"
    
    class Meta:
        db_table = 'hub_models'
        ordering = ['-created_at']

class AddressModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='user_address', on_delete=models.CASCADE, blank=True, null=True)
    division = models.ForeignKey(DivisionModel, related_name='division_address', blank=True, null=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(DistrictModel, related_name='district_address', blank=True, null=True, on_delete=models.SET_NULL)
    sub_district = models.ForeignKey(SubDistrictModel, related_name='thana_address', blank=True, null=True, on_delete=models.SET_NULL)
    area = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    house = models.CharField(max_length=100, blank=True, null=True)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True, choices=AddressLabelType)
    label_name = models.CharField(max_length=50, blank=True, null=True)
    map = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''} -- {self.label_name if self.label_name else ''}"

    class Meta:
        db_table = 'address_models'
        ordering = ['-created_at']
