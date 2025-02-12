import re

from rest_framework.validators import ValidationError


def username_validation(value):
    if value.lower() == 'me':
        raise ValidationError("Недопустимое имя пользователя: 'me'.")

    if re.fullmatch(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError("Имя пользователя содержит недопустимые символы")

    return value
