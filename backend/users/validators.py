import re

from rest_framework.validators import ValidationError


def username_validation(value):
    if re.fullmatch(r"^[\w.@+-]+$", value) is None:
        raise ValidationError("Недопустимые символы в username.")
