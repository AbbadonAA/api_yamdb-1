from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def this_year():
    return datetime.now().year


def max_value_this_year(value):
    return MaxValueValidator(
        this_year(),
        'Нельзя добавлять произведения из будущего.'
    )(value)


def min_value_first_year(value):
    return MinValueValidator(
        1,
        'Нельзя добавлять произведения до нашей эры. :)'
    )(value)
