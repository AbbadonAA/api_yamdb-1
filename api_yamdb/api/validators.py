from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError
)

from titcatgen.models import Category, Genre, Title
from reviews.models import Review, Comment


def validate(self):
    request = self.context['request']
    title_id = self.context.get('view').kwargs.get('title_id')
    title = get_object_or_404(Title, pk=title_id)
    if (
        request.method == 'POST'
        and Review.objects.filter(
            title=title,
            author=request.user
        ).exists()
    ):
        raise ValidationError('Один отзыв, не более!')

def author(self):
    request = self.context['request']
    title_id = self.context.get('view').kwargs.get('title_id')
    title = get_object_or_404(Title, pk=title_id)
    if (
        request.method == 'POST'
        and Review.objects.filter(
            title=title,
            author=request.user
        ).exists()
    ):
        raise ValidationError('Один отзыв, не более!')


def one(value):
    if Review.objects.filter(title=value).exists():
        raise ValidationError('Один отзыв, не более!')

def two(value):
    if Review.objects.filter(author=value).exists():
        raise ValidationError('Один отзыв, не более!')

def three(author, title):
    if (Review.objects.filter(author=author).exists() and
        Review.objects.filter(title=title).exists()):
        raise ValidationError('Один отзыв, не более!')