from datetime import datetime
from django.db.models import Avg
from rest_framework.serializers import (
    CurrentUserDefault,
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
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = datetime.now().year
        if not 0 <= value <= current_year:
            raise ValidationError(
                'Проверьте год создания произведения (должен быть нашей эры).'
            )
        return value


class TitleSerializer(ModelSerializer):
    rating = SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)

# class TitleSerializer(ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(read_only=True, many=True)
#     rating = SerializerMethodField()

#     class Meta:
#         fields = (
#             'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
#         read_only_fields = ('id', 'rating')
#         model = Title

#     def validate_year(self, year):
#         if year > datetime.now().year:
#             raise ValidationError(
#                 'Нельзя добавлять произведения из будущего.')
#         return year
    
#     def get_rating(self, obj):
#         rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
#         if not rating:
#             return rating
#         return round(rating, 1)




# class ReviewSerializer(ModelSerializer):
#     author = SlugRelatedField(
#         slug_field='username', read_only=True, default=CurrentUserDefault())

#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'author', 'score', 'pub_date',)
#         read_only_fields = ('id', 'pub_date')

#     def validate(self, data):
#         if self.context['request'].method != 'POST':
#             return data
#         title_id = (self.context['request'].path).split('/')[4]
#         author = self.context['request'].user
#         if Review.objects.values(
#             'author', 'title').filter(
#                 author=author, title__id=title_id).exists():
#             raise ValidationError('Вы уже написали отзыв.')
#         return data
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
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review

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
