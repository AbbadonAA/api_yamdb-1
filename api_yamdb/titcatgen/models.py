from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def this_year():
    return datetime.now().year


def max_value_this_year(value):
    return MaxValueValidator(
        this_year(),
        'Нельзя добавлять произведения из будущего.'
    )(value)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        validators=[
            max_value_this_year,
            MinValueValidator(
                1,
                'Наша эра начинается с первого года.'
            ),
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )
    description = models.TextField(blank=True,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name