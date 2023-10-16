# Бэкенд веб-приложения для управления разрешением споров и конфликтных ситуаций среди сотрудников

## Структура проекта:

| Имя  | Описание |
| ------------- | ------------- |
| src | Файлы для backend разработки |
| infra | Docker-compose файлы для запуска проекта с помощью Docker |


## Правила работы с git (как делать коммиты и pull request-ы):

1. Две основные ветки: `main` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. В `main` находится только production-ready код (CI/CD)
4. Создавая новую ветку, наследуйтесь от ветки `develop`
5. Правила именования веток
   - весь новый функционал — `feature/название-функционала`
   - исправление ошибок — `bugfix/название-багфикса`
6. Пушим свою ветку в репозиторий и открываем Pull Request


## Запуск приложения в контейнерах:

Для запуска приложения в контейнерах необходимо:

1. Клонировать репозиторий и перейти в директорию с файлом *.env.example*:
```
git clone git@github.com:management-of-dispute-resolution/dispute_resolution_backend.git
```
```
cd dispute_resolution_backend/
```

2. Создать файл .env с переменными окружения из *.env.example*. Пример наполнения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

3. Перейти в директорию с файлом *docker-compose.yaml*, открыть терминал и запустить docker-compose с ключом `-d`:
```
cd infra/
```
```
docker-compose up -d
```

4. Выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```

5. Создать суперюзера:
```
docker-compose exec backend python manage.py createsuperuser
```

6. Собрать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

7. После успешного запуска проект станет доступен по адресу:
http://localhost/

8. Остановить проект:
```
docker-compose down
```

9. Если необходимо пересобрать контейнеры после изменений в проекте:
```
docker-compose up -d --build
```
