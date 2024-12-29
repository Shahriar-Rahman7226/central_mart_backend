from django.contrib import admin
from apps.product_management.models import *

# Register your models here.
admin.site.register(CategoryModel)
admin.site.register(SubCategoryModel)
admin.site.register(ProductModel)
admin.site.register(ProductImageModel)