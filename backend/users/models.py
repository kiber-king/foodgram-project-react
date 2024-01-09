from django.contrib.auth.models import AbstractUser
from django.db import models

from core import validators
from core import constants


class User(AbstractUser):
    """Custom модель пользователя."""

    email = models.EmailField(
        verbose_name='Email',
        max_length=constants.MAX_EMAEL_LENGHT,
        unique=True,
        help_text='Введите адрес электронной почты.',
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=constants.MAX_USER_LENGHT,
        unique=True,
        help_text='Введите ник пользователя',
        validators=(
            validators.validate_username,
            validators.LatinCharRegexValidator(
                message='Имя пользователя должно'
                        ' содержать только латиницу и нижние подчеркивания.'),
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        )
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свое имя',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(
                message='Имя должно содержать только кириллические '
                        'символы.')
        )
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свою фамилию',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(
                message='Фамилия должна содержать только кириллические '
                        'символы.')
        )
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свой пароль'

    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='unique_username_email',
            ),
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки на другого пользователя"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='subscriber_user',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор в подписке',
        related_name='author_in_subscription',
        on_delete=models.CASCADE,
    )
    subscription_date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now=True,
    )

    class Meta:
        ordering = ('subscription_date',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author', ],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user_id=models.F('author_id')),
                name='no_self_subscription'
            ),
        )

    def __str__(self):
        return (
            f'{self.user} подписан на {self.author}'
        )
