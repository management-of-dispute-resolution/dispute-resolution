from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        abstract = True


class Dispute(BaseModel):
    """Dispute model."""

    MAX_LENGTH_TITLE = 50
    MAX_LENGTH_STATUS = 20

    STARTED = 'started'
    CLOSED = 'closed'
    NOT_STARTED = 'not_started'

    DISPUTE_STATUS = [
        (STARTED, 'Решается'),
        (CLOSED, 'Решено'),
        (NOT_STARTED, 'Не рассмотрено'),
    ]

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disputes_creator',
        verbose_name='Создатель',
    )
    description = models.TextField(verbose_name='Описание')
    closed_at = models.DateTimeField(
        verbose_name='Время закрытия',
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=DISPUTE_STATUS,
        default=NOT_STARTED,
        verbose_name='Статус обращения',
    )
    opponent = models.ManyToManyField(
        User,
        related_name='disputes_opponent',
        verbose_name='Оппонент',
    )
    add_opponent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Спор'
        verbose_name_plural = 'Споры'

    def __str__(self):
        return f'Спор от {self.creator}'


class Comment(BaseModel):
    """Comment model."""

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отправитель',
    )
    content = models.TextField(verbose_name='Описание')
    dispute = models.ForeignKey(
        Dispute,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='спор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.sender}'


class File(models.Model):
    """Abstract model for files."""

    file = models.FileField(
        upload_to='uploads/',
        blank=True,
        null=True,
        verbose_name='Файл',
    )

    class Meta:
        abstract = True


class FileDispute(File):
    """File of dispute model."""

    dispute = models.ForeignKey(
        Dispute,
        on_delete=models.CASCADE,
        related_name='file'
    )

    def __str__(self):
        return f'Файл в {self.dispute}'


class FileComment(File):
    """File of comment model."""

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='file'
    )

    def __str__(self):
        return f'Файл в {self.comment}'
