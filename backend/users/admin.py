from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ панель модели пользователя."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'count_following',
        'count_recipe',
    )
    list_filter = (
        'email',
        'username',
    )

    @admin.display(description='Количество подписок')
    def count_following(self, obj):
        return obj.author_in_subscription.count()

    @admin.display(description='Количество рецептов в избранном')
    def count_recipe(self, obj):
        return obj.recipe_author.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админ панель модели подписки."""

    list_display = (
        'user',
        'author',
        'subscription_date',
    )
    list_filter = (
        'user',
        'author',
    )
