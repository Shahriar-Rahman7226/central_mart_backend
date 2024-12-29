import uuid
from django.db.models import Model, BooleanField, DateTimeField, UUIDField, Manager


class ActiveManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DeactivateManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class CustomModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True,
                   help_text="Unique id for a model's object")
    is_active = BooleanField(default=True, db_index=True, help_text="Is the model's object active")
    created_at = DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")
    updated_at = DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")

    objects = Manager()

    class Meta:
        abstract = True
