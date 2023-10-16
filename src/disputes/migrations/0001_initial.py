# Generated by Django 4.1 on 2023-10-15 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл')),
                ('description', models.TextField(verbose_name='Описание')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('status', models.CharField(choices=[('stated', 'Решается'), ('closed', 'Решено'), ('not_started', 'Не рассмотрено')], max_length=20, verbose_name='Статус обращения')),
                ('add_opponent', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputes_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('next_commentator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disputes_commentator', to=settings.AUTH_USER_MODEL, verbose_name='Следующий комментатор')),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputes_opponent', to=settings.AUTH_USER_MODEL, verbose_name='Оппонент')),
            ],
            options={
                'verbose_name': 'Спор',
                'verbose_name_plural': 'Споры',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл')),
                ('content', models.TextField(verbose_name='Описание')),
                ('dispute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='disputes.dispute', verbose_name='спор')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='отправитель')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
