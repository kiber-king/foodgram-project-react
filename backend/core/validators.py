from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator)


class MinTagColorLenghtValidator(MinLengthValidator):
    message = 'Цвет должен состоять минимум из 4 символов!'


class MinMeasurementUnitLenghtValidator(MinLengthValidator):
    message = 'Единица измерения может состоять минимум из одного символа!'


class TwoCharValidator(MinLengthValidator):
    message = 'Длина должна быть больше 2 символов'


class MinCookingTimeValueValidator(MinValueValidator):

    message = 'Время готовки должно быть не меньше одной минуты.'


class MaxCookingTimeValueValidator(MaxValueValidator):

    message = 'Время готовки должно быть не больше 500 минут.'


class MinAmountValidator(MinValueValidator):

    message = 'Количество игредиента не может быть меньше единицы.'


class MaxAmountValidator(MaxValueValidator):

    message = 'Количество игредиента не может быть больше 999 единиц.'


class CyrillicCharRegexValidator(RegexValidator):
    regex = '^[А-Яа-я ,-.()]+$'
    message = (
        'Разрешена только криллица. Могут использоваться '
        'только буквы и пробелы, тире, запятые, точки, скобки.'
    )
    code = 'Invalid char not cirilic'


class TagColorRegexValidator(RegexValidator):
    regex = '^#[0-9A-Fa-f]{3}$|^#[0-9A-Fa-f]{6}$'
    message = (
        'Цвет должен начинаться с символа # и '
        'может состоять только из цифр 0-9'
        'и латинских букв A-F или a-f. Длина 4 или 7 символов.'
    )
    code = 'Invalid tag HEX color'


class LatinCharRegexValidator(RegexValidator):
    regex = '^[A-Za-z_]+$'
    message = (
        'Допускается только латиница '
        'и нижние подчеркивания.'
    )
    code = 'Invalid char not latin'


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('username не может быть "me"')
    return value


def validate_recipe_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Название рецепта не должно содержать цифр')
    return value
