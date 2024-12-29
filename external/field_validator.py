from django.core.exceptions import ValidationError


def validate_permission(value):
    valid_permissions = ['C', 'R', 'U', 'D', 'A', 'N']
    for char in value:
        if char.upper() not in valid_permissions:
            raise ValidationError(
                f"{char} is not a valid permission. Valid permissions are: {', '.join(valid_permissions)}"
            )
