from django.contrib import admin

from apps.address.models import *

# Register your models here.
@admin.register(DivisionModel)
class DivisionModelAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(DistrictModel)
class DistrictModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'division'] 

@admin.register(SubDistrictModel)
class SubDistrictModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'division', 'district'] 

@admin.register(AddressModel)
class AddressModelAdmin(admin.ModelAdmin):
    search_fields = ['division', 'district', 'thana'] 

admin.site.register(HubModel)
