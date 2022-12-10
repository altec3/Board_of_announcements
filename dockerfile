FROM python:3.10-slim

ARG DB_ENGINE="django.db.backends.postgresql"
ARG DB_NAME="postgres"
ARG DB_USER="postgres"
ARG DB_PASSWORD="postgres"
ARG DB_HOST="localhost"
ARG DJANGO_SK="(-s6z3ftm4ac)&s6!dcg)7@76=t6x=kz=-u2anu7r@bkg7_7g+"
ARG DJANGO_DEBUG=1
ARG EMAIL_USE_TLS=1
ARG EMAIL_USE_SSL=0
ARG EMAIL_HOST="smtp.gmail.com"
ARG EMAIL_HOST_USER="example@gmail.com"
ARG EMAIL_HOST_PASSWORD="password"
ARG EMAIL_PORT=587

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SK="${DJANGO_SK}" \
    DJANGO_DEBUG="${DJANGO_DEBUG}" \
    DB_ENGINE="${DB_ENGINE}" \
    DB_NAME="${DB_NAME}" \
    DB_USER="${DB_USER}" \
    DB_PASSWORD="${DB_PASSWORD}" \
    DB_HOST="${DB_HOST}"\
    EMAIL_USE_TLS="${EMAIL_USE_TLS}" \
    EMAIL_USE_SSL="${EMAIL_USE_SSL}" \
    EMAIL_HOST="${EMAIL_HOST}" \
    EMAIL_HOST_USER="${EMAIL_HOST_USER}" \
    EMAIL_HOST_PASSWORD="${EMAIL_HOST_PASSWORD}" \
    EMAIL_PORT="${EMAIL_PORT}"

WORKDIR /coursework

# Установка зависимостей
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install --no-cache-dir --no-warn-script-location -U pip &&\
    pip install --no-cache-dir --no-warn-script-location poetry &&\
    poetry config virtualenvs.create false &&\
    poetry install

# Копирование файлов проекта
COPY skymarket/manage.py .
COPY skymarket/ads ads
COPY skymarket/django_media django_media
COPY skymarket/django_static django_static
COPY skymarket/redoc redoc
COPY skymarket/skymarket skymarket
COPY skymarket/users users
COPY entrypoint.sh entrypoint.sh

# Загрузка фикстур
ENTRYPOINT ["bash", "entrypoint.sh"]
