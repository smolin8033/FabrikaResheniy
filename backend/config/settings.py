import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Questions
# pre-commit install
# error: cannot format backend/mailing/migrations/0003_alter_mailing_managers.py: [Errno 13] Permission denied: 'backend/mailing/migrations/0003_alter_mailing_managers.py'
# UnicodeDecodeError: 'utf-16-le' codec can't decode byte 0x0a in position 1180: truncated data
# executor failed running [/bin/sh -c pip install -r requirements.txt]: exit code: 2
# ^backend/.*.(py|pyi)$
# должны быть такие большие блоки кода в тестах
# вопросы по полям в фабриках

# .*.
# переопределить базу данных запускать локалхост
# прокинуть postgres
# ctrl alt o
# ctrl d


# TODO env
# TODO testing big data factories boy
# TODO do testing
# TODO turn off endpoints???
# TODO deploy
# TODO добавить nginx gunicorn

"""
Check прокидывание портов постгресс
Check https://stackoverflow.com/questions/17843630/python-can-dumpdata-cannot-loaddata-back-unicodedecodeerror
Check isort и pre-commit (black) как будто противоречат друг другу


-- обновления атрибутов рассылки
-- (сложный случай: отправить запрос на внешний сервис подделать внешний сервис + pytest monkey patch (менять request - всегда ответ ок) +)
-- HARD После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания - должны быть выбраны из справочника все клиенты, которые подходят под значения фильтра, указанного в этой рассылке и запущена отправка для всех этих клиентов.
-- получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
-- (проверять, работает ли селери, фикстура mock) HARD
-- получения детальной статистики отправленных сообщений по конкретной рассылке HARD

-- env/secret key / docker-compose
-- nginx gunicorn
-- купить сервер
"""

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "mailing.apps.MailingConfig",
    "customer.apps.CustomerConfig",
    "message.apps.MessageConfig",
    # side-packages
    "rest_framework",
    "drf_spectacular",
    "debug_toolbar",
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "notifications",
        "USER": "admin_notifications",
        "PASSWORD": "admin",
        "HOST": "postgres",
        "PORT": "5432",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


INTERNAL_IPS = [
    "127.0.0.1",
]


DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
