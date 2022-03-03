from django.db.models import Avg
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError
)
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.relations import SlugRelatedField

from titcatgen.models import Category, Genre, Title
from reviews.models import Review, Comment
from users.models import User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleCreateSerializer(ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(ModelSerializer):
    rating = SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.reviews.aggregate(average=Avg('score'))['average']


class ReviewSerializer(ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Один отзыв, не более!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
