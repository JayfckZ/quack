from django.core.exceptions import ValidationError
import re

def validate_handle(value):
    if not re.match(r'^[a-zA-Z0-9-_]+$', value):
        raise ValidationError(
            'Handle deve conter apenas letras, números, "-" e "_".'
        )
