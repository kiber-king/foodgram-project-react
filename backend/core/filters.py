from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


def get_queryset_filter(queryset, user, value, relation):
    if user.is_anonymous:
        return queryset
    if bool(value):
        return queryset.filter(**{relation: user})
    return queryset.exclude(**{relation: user})


class IngredientFilter(FilterSet):
    """Фильтрация ингредиентов по названию"""
    name = filters.CharFilter(method='ingredient_name_filter')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def ingredient_name_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__startswith=value) | Q(name__contains=value)
        )


class RecipeFilter(FilterSet):
    """Фильтрация рецептов"""
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def is_favorited_filter(self, queryset, name, value):
        return get_queryset_filter(
            queryset=queryset,
            user=self.request.user,
            value=value,
            relation='favorites__user'
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return get_queryset_filter(
            queryset=queryset,
            user=self.request.user,
            value=value,
            relation='shopping_cart__user'
        )
