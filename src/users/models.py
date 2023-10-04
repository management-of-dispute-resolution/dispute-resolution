from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from config.settings import USER_FIELD


class CustomUser(AbstractUser):
    USER = 'user'
    PSICHOLOG = 'psicholog'
    ADMINISTRATOR = 'admin'

    USER_ROLES = [
        (USER, 'user'),
        (PSICHOLOG, 'psicholog'),
        (ADMINISTRATOR, 'admin'),
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
    image = models.ImageField(
        # upload_to='users_images',
        blank=True,
        null=True,
        verbose_name='Фото'
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
    def is_psicholog(self):
        return self.role == 'psicholog'

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username')
        verbose_name = 'Участник сообщества'
        verbose_name_plural = 'Участники сообщества'
