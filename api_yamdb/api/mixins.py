from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from .permissions import AdminAuthorizedOrReadOnly


class CategoryGenreMixinViewSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        GenericViewSet):
    queryset = None
    serializer_class = None
    filter_backends = [SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = (AdminAuthorizedOrReadOnly,)
    pagination_class = PageNumberPagination
