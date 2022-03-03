from django.core import validators


def validate_score(value):
    if 0 > value > 10:
        raise validators.BaseValidator('0-10')
    return value
