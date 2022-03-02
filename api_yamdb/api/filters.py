from django_filters.rest_framework import BaseInFilter, CharFilter, FilterSet

from titcatgen.models import Title


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class TitleFilter(FilterSet):
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')