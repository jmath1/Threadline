"""
Django settings for db_project project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import logging
import os
from pathlib import Path
import sys
from mongoengine import connect

IS_TESTING = "test" in sys.argv

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^a%1(5g9*c^k56jv(v8y5&fmzx83toi3p3u&qjw#$6x+r+z)^r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0"]


AUTH_USER_MODEL = 'main.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "corsheaders",
    "main",
    "crispy_forms",
    "crispy_bootstrap4",
    "rest_framework",
    "rest_framework_gis",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.middleware.logging_middleware.LoggingMiddleware"
]

CORS_ALLOWED_ORIGINS = [
    'http://0.0.0.0:3000',
    'http://localhost:3000',
    'http://0.0.0.0:8000',
]
CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = "db_project.urls"

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

WSGI_APPLICATION = "db_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'project1',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': os.getenv("POSTGRES_HOST",'postgres'),
        'PORT': '5432',
        'MIGRATE': True,    
        'TEST': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'test',
            'ALIAS': 'test',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': os.getenv("POSTGRES_HOST",'postgres'),
            'PORT': '5432',
            'MIGRATE': True
        }}
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

JWT_EXPIRATION_TIME = 60000 # 10 minutes

TEST_RUNNER = 'main.runners.GISDataTestRunner'


CELERY_BROKER_URL = os.getenv('CELERY_BROKER',f'redis://{os.getenv("REDIS_HOST", "redis")}:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


if os.getenv("LOGGING_HOST"):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s"}',
            },
        },
        'handlers': {
            'logstash': {
                'level': 'DEBUG',
                'class': 'logging.handlers.SocketHandler',
                'host': os.getenv('LOGGING_HOST', '0.0.0.0'),
                'port': int(os.getenv('LOGGING_PORT', 5044)),
                'formatter': 'json',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logstash'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }


# MongoDB Connection
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)

if IS_TESTING:
    MONGO_DATABASE_NAME = "test"
else:
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "messages_db")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE_NAME}"
connect(
    MONGO_DATABASE_NAME,
    host=MONGO_URI
)