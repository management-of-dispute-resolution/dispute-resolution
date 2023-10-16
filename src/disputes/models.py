from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    file = models.FileField(
        # upload_to='uploads/',
        blank=True,
        null=True,
        verbose_name='Файл',
    )

    class Meta:
        abstract = True


class Dispute(BaseModel):
    """Dispute model."""

    MAX_LENGTH_TITLE = 50
    MAX_LENGTH_STATUS = 20

    STARTED = 'stated'
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
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Заголовок',
    )
    edited_at = models.DateTimeField(
        auto_now=True, verbose_name='Время изменения'
    )
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=DISPUTE_STATUS,
        verbose_name='Статус обращения',
    )
    opponent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disputes_opponent',
        verbose_name='Оппонент',
    )
    next_commentator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='disputes_commentator',
        verbose_name='Следующий комментатор',
    )
    add_opponent = models.BooleanField(default=False)

    class Meta:
        models.UniqueConstraint(
            fields=['creator', 'opponent'], name='unique_users'
        )
        verbose_name = 'Спор'
        verbose_name_plural = 'Споры'

    def __str__(self):
        return self.title


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
