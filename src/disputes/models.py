from django.contrib.auth import get_user_model as User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        abstract = True


class Dispute(BaseModel):
    MAX_LENGTH_TITLE = 255
    MAX_LENGTH_CRITICALITY = 10

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CRITICALITY_CHOICES = [
        (LOW, 'Низкая'),
        (MEDIUM, 'Средняя'),
        (HIGH, 'Высокая'),
    ]

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disputes',
        verbose_name='Создатель',
    )
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    criticality = models.CharField(
        max_length=MAX_LENGTH_CRITICALITY,
        choices=CRITICALITY_CHOICES,
        verbose_name='Критичность',
    )
    target_date = models.DateTimeField(verbose_name='Контрольный срок')
    participants = models.ManyToManyField(
        User,
        through='DisputeParticipants',
        verbose_name='Участники',
    )

    class Meta:
        abstract = False
        verbose_name = 'Спор'
        verbose_name_plural = 'Споры'

    def __str__(self):
        return self.title


class DisputeParticipants(models.Model):
    MAX_LENGTH_ROLE = 20

    CREATOR = 'creator'
    RECIPIENT = 'recipient'
    PSYCHOLOGIST = 'psychologist'

    ROLE_CHOICES = [
        (CREATOR, 'Создатель'),
        (RECIPIENT, 'Адресат'),
        (PSYCHOLOGIST, 'Психолог'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    dispute = models.ForeignKey(
        Dispute,
        on_delete=models.CASCADE,
        verbose_name='Спор',
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Участник спора'
        verbose_name_plural = 'Участники спора'

    def __str__(self):
        return f'Спор {self.dispute}: {self.user} - {self.role}'


class Message(BaseModel):
    dispute = models.ForeignKey(
        Dispute,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Спор',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Отправитель',
    )
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        abstract = False
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Спор {self.dispute}: {self.sender} - {self.content}'


class Attachment(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Сообщение'
    )
    file = models.FileField(
        # upload_to='attachments/',
        blank=True,
        null=True,
        verbose_name='Файл',
    )

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
