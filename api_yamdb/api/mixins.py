from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from api.permissions import AdminOrReadOnly


class CategoryGenreMixinViewSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        GenericViewSet):
    """Миксин для классов жанра и категории."""
    queryset = None
    serializer_class = None
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination