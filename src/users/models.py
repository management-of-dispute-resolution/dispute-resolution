from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from config.settings import USER_FIELD


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    This manager provides custom methods
    for creating regular users and superusers.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Private method.

        Creates and saves a CustomUser
        with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create a regular user with the given email and password.

        Uses _create_user.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with the given email and password.

        Uses _create_user.
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model."""

    USER = 'user'
    MEDIATOR = 'mediator'
    ADMINISTRATOR = 'admin'

    USER_ROLES = [
        (USER, 'Пользователь'),
        (MEDIATOR, 'Медиатор'),
        (ADMINISTRATOR, 'Администратор'),
    ]
    email = models.EmailField(
        max_length=USER_FIELD,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты',
    )
    # Change USERNAME_FIELD to 'email'
    USERNAME_FIELD = 'email'

    # Update of REQUIRED_FIELDS
    REQUIRED_FIELDS = ['password']

    # Connects CustomUser model with CustomUserManager
    objects = CustomUserManager()

    first_name = models.CharField(
        verbose_name='Имя', max_length=USER_FIELD, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=USER_FIELD, blank=True
    )
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Номер телефона может состоять только из цифр',
            )
        ],
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=USER_FIELD,
        choices=USER_ROLES,
        default=USER,
    )

    @property
    def is_user(self):
        """Check the role 'user'."""
        return self.role == 'user'

    @property
    def is_admin(self):
        """Check the role 'admin'."""
        return self.role == 'admin'

    @property
    def is_mediator(self):
        """Check the role 'mediator'."""
        return self.role == 'mediator'

    class Meta:
        ordering = ('email',)
        verbose_name = 'Участник сообщества'
        verbose_name_plural = 'Участники сообщества'

    def __str__(self):
        return self.email
