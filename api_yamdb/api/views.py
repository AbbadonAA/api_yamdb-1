from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import CategoryGenreMixinViewSet
from api.permissions import (AdminOrReadOnly,
                             AuthorStaffOrReadOnly,
                             IsAuthorOrReadOnly,
                             IsRoleAdmin,
                             IsRoleModerator,
                             AdminOnly,)
from .serializers import (GetTokenSerializer,
                          NotAdminSerializer,
                          SignUpSerializer,
                          UsersSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          TitleCreateSerializer)
from titcatgen.models import Category, Genre, Title
from reviews.models import Review
from users.models import User


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    # def perform_create(self, serializer):
    #     category_slug = self.request.data['category']
    #     category = get_object_or_404(Category, slug=category_slug)
    #     genre_slug = self.request.POST.getlist('genre')
    #     genres = Genre.objects.filter(slug__in=genre_slug)
    #     serializer.save(
    #         category=category,
    #         genre=genres,
    #     )

    # def perform_update(self, serializer):
    #     category_slug = self.request.data['category']
    #     category = get_object_or_404(Category, slug=category_slug)
    #     genre_slug = self.request.POST.getlist('genre')
    #     genres = Genre.objects.filter(slug__in=genre_slug)
    #     serializer.save(
    #         category=category,
    #         genre=genres,
    #     )
    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(CategoryGenreMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = (AuthorStaffOrReadOnly,)

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()

#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (AuthorStaffOrReadOnly,)

#     def get_queryset(self):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         return review.comments.all()

#     def perform_create(self, serializer):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         serializer.save(author=self.request.user, review=review)

# class ReviewViewSet(ModelViewSet):
#     """
#     Admin, Moderator can manage reviews
#     User can manage self reviews
#     /titles/{title_id}/reviews/ - get all reviews on title
#     /titles/{title_id}/reviews/{id}/ - get title with id
#     """
#     serializer_class = ReviewSerializer
#     permission_classes = (
#         AuthorStaffOrReadOnly,
#     )

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()

#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         serializer.save(author=self.request.user, title=title)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)