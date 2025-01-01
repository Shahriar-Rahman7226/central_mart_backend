from django.db import models
from abstract.base_model import CustomModel
from apps.users.models import UserModel

# Create your models here.
class BannerModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='banner/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title if self.title else ''}"

    class Meta:
        db_table = 'banner'
        ordering = ["-created_at"]


class FAQModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='faq_user', on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    asnwer = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''}"
    
    class Meta:
        db_table='faq_model'
        ordering=['-created_at']


class LegalDocument(CustomModel):
    details = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    licence_document = models.FileField(blank=True, null=True)

    class Meta:
        db_table='legal_document'
        ordering=['-created_at']


class PrivacyPolicy(CustomModel):
    details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='privacy_policy'
        ordering=['-created_at']


class AboutUs(CustomModel):
    introduction = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    class Meta:
        db_table='about_us'
        ordering=['-created_at']


class FooterModel(CustomModel):
    image = models.ImageField(upload_to='footer/', blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    class Meta:
        db_table='footer_models'
        ordering=['-created_at']
