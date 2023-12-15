from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from core import validators
from core import constants

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        help_text='Придумай название для тега',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    color = ColorField(
        verbose_name='Цвет в HEX',
        max_length=constants.MAX_TAG_COLOR_LENGHT,
        help_text='Пропишите цвет в HEX формате',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        help_text='Введите слаг тега',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.LatinCharRegexValidator(),
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(
        db_index=True,
        verbose_name='Название ингредиента',
        help_text='Напишите название ингредиента',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        ),
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        help_text='Введите единицу измерения',
        validators=(
            validators.MinMeasurementUnitLenghtValidator(
                constants.MIN_MEASUREMENT_UNIT_LENGHT
            ),
            validators.CyrillicCharRegexValidator()
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'name',
                    'measurement_unit',
                ],
                name='unique_name_measurement_unit',
            ),
        )

    def __str__(self):
        return (
            f'{self.name}, {self.measurement_unit}.'
        )


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipe_author',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        help_text='Придумайте название рецепта',
        validators=(
            validators.validate_recipe_name,
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        ),
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Опишите рецепт',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        ),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='ingredients_in_recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Выбирете теги для рецепта',
        related_name='recipe_tags',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Введите время приготовления рецепта',
        validators=(
            validators.MinCookingTimeValueValidator(
                constants.MIN_COOKING_TIME
            ),
            validators.MaxCookingTimeValueValidator(
                constants.MAX_COOKING_TIME
            )
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', 'name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}, автор {self.author.username}.'


class RecipeIngredientAmount(models.Model):
    """Модель ингредиентов в рецепте"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinAmountValidator(
                constants.MIN_AMOUNT
            ),
            validators.MaxAmountValidator(
                constants.MAX_AMOUNT
            )
        )
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient',
                ],
                name='unique_recipe_ingredient',
            ),
        )
        ordering = ('recipe', 'ingredient',)
        verbose_name = 'Количество ингредиента в рецепте'

    def __str__(self):
        return (
            f'В {self.recipe.name} содержится '
            f'{self.amount}{self.ingredient.measurement_unit}. '
            f'{self.ingredient.name}.'
        )


class AbstractUsersRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(app_label)s_%(class)s_unique'
            )
        ]

    def str(self):
        return f'{self.user} :: {self.recipe}'


class FavoriteRecipe(AbstractUsersRecipe):
    """Модель  избранных рецептов"""
    add_to_favorite_date = models.DateTimeField(
        verbose_name='Дата добавления в избранное',
        auto_now=True,
    )

    class Meta(AbstractUsersRecipe.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('add_to_favorite_date',)


class Cart(AbstractUsersRecipe):
    """Модель списка покупок"""
    add_to_shopping_cart_date = models.DateTimeField(
        verbose_name='Дата добавления в корзину',
        auto_now=True,
    )

    class Meta(AbstractUsersRecipe.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        ordering = ('-id',)
