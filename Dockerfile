FROM python:3.11-slim

WORKDIR /app

COPY src/ /app

COPY .env /app

RUN pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
