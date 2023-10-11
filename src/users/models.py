from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from config.settings import USER_FIELD


class CustomUser(AbstractUser):
    USER = 'user'
    MEDIATOR = 'mediator'
    ADMINISTRATOR = 'admin'

    USER_ROLES = [
        (USER, 'Пользователь'),
        (MEDIATOR, 'Медиатор'),
        (ADMINISTRATOR, 'Администратор'),
    ]
    username = models.CharField(
        max_length=USER_FIELD,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Имя на сайте',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        max_length=USER_FIELD,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_FIELD,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_FIELD,
        blank=True
    )
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d+$',
            message='Номер телефона может состоять только из цифр'
        )]
    )
    department = models.CharField(
        verbose_name='Отдел',
        max_length=USER_FIELD
    )
    post = models.CharField(
        blank=False,
        null=False,
        verbose_name='Должность',
        max_length=USER_FIELD
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=USER_FIELD,
        choices=USER_ROLES,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_mediator(self):
        return self.role == 'mediator'

    class Meta:
        ordering = ('username')
        verbose_name = 'Участник сообщества'
        verbose_name_plural = 'Участники сообщества'

    def __str__(self):
        return self.username
