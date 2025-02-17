import re

from rest_framework.validators import ValidationError


def username_validation(value):
    if re.fullmatch(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError("Недопустимые символы в username.")

    if "me" in value.lower():
        raise ValidationError("Использование 'me' в username запрещено.")
