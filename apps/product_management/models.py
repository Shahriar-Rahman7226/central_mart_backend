from django.db import models
from external.choice_tuple import WeightUnit
from abstract.base_model import CustomModel
from apps.address.models import HubModel


# Create your models here.
class CategoryModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title if self.title else ''}"

    class Meta:
        db_table = 'category_models'
        ordering = ['-created_at']


class SubCategoryModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='subcategory/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(CategoryModel, related_name='subcategory_category', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.title if self.title else ''} -- {self.category.title if self.category else ''}"

    class Meta:
        db_table = 'subcategory_models'
        ordering = ['-created_at']


class ProductModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(CategoryModel, related_name='product_category', on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategoryModel, related_name='product_subcategory', on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    hub = models.ForeignKey(HubModel, related_name='product_hub', on_delete=models.SET_NULL, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(max_length=50, blank=True, null=True, choices=WeightUnit)
    in_stock = models.BooleanField(blank=True, null=True, default=True)
    stock_level = models.PositiveIntegerField(blank=True, null=True)
    cost_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True, null=True)
    offered_price = models.FloatField(blank=True, null=True)
    gross_profit = models.FloatField(blank=True, null=True)
    profit_margin = models.FloatField(blank=True, null=True, help_text="Profit margin of the product (in percentage)")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    featured_details = models.TextField(blank=True, null=True)
    order_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    promotion_tag = models.CharField(max_length=100, blank=True, null=True)
   

    def __str__(self):
        return f"{self.title if self.title else ''} -- {self.subcategory.title if self.subcategory else ''} -- {self.category.title if self.category else ''} -- {self.hub.name if self.hub else ''}"

    class Meta:
        db_table = 'product_models'
        ordering = ['-created_at']


class ProductImageModel(CustomModel):
    product = models.ForeignKey(ProductModel, related_name='product_image', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='product/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.title if self.product else ''}"

    class Meta:
        db_table = 'product_image_models'
        ordering = ['-created_at']