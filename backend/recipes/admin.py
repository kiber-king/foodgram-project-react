from django.contrib import admin

from recipes.models import (Cart, FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredientAmount, Tag)


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 1
    min_num = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ панель списка покупок."""

    list_display = (
        'user',
        'recipe',
        'get_ingredients',
        'add_to_shopping_cart_date',
    )
    list_filter = (
        'user',
        'recipe',
    )

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return '\n'.join(
            ingredient.name for ingredient in obj.recipe.ingredients.all()
        )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Админ панель избранных рецептов."""

    list_display = (
        'user',
        'recipe',
        'add_to_favorite_date',
    )
    list_filter = (
        'user',
        'recipe',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ панель модели ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ панель модели рецептов."""

    list_display = (
        'name',
        'author',
        'in_favorite_count',
        'get_ingredients',
        'get_tags',
    )
    list_filter = (
        'author__username',
        'name',
        'tags',
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )
    readonly_fields = (
        'in_favorite_count',
    )
    inlines = (
        RecipeIngredientAmountInline,
    )

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ',\n'.join(
            ingredient.name for ingredient in obj.ingredients.all()
        )

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return '\n'.join(
            tag.name for tag in obj.tags.all()
        )

    @admin.display(description='Кол-во добавлений')
    def in_favorite_count(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    """Админ панель добавления ингредиента в рецепт."""

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ панель модели тегов."""

    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
    )
