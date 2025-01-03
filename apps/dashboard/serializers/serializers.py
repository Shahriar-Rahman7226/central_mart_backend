from rest_framework import serializers
from core import settings
from apps.dashboard.models import BannerModel

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class BannerSerializer(serializers.ModelSerializer):
    # Override the image field to include the full URL
    image = serializers.SerializerMethodField()

    class Meta:
        model = BannerModel
        exclude = exclude_list

    def get_image(self, obj):
        # Check if the image exists and construct the full URL
        if obj.image:
            return f"{settings.SITE_URL}{obj.image.url}"  # Using SITE_URL to get the full URL
        return None  # Return None if there's no image
