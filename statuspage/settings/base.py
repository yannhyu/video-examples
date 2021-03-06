"""
Django settings for statuspage project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pathlib

# Global environment defaults
os.environ.setdefault('BASE_DIR', str(pathlib.Path(__file__).parents[2]))

BASE_DIR = os.environ['BASE_DIR']

os.environ.setdefault(
    'DATABASE_URL',
    'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3')))
os.environ.setdefault(
    'BROKER_URL',
    'amqp://guest:guest@localhost:5672/')

# Application definition

INSTALLED_APPS = (
    'statuspage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'domainchecks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'statuspage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'statuspage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(),
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Authentication settings

LOGIN_URL = '/login/'

LOGOUT_URL = '/logout/'

LOGIN_REDIRECT_URL = '/'

# Celery settings

from celery.schedules import crontab

BROKER_URL = os.environ['BROKER_URL']

CELERY_RESULT_BACKEND = None

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ('json', )

CELERY_TIMEZONE = TIME_ZONE

CELERYBEAT_SCHEDULE = {
    'update-domains': {
        'task': 'domainchecks.tasks.queue_domains',
        'kwargs': {'minutes': 2},
        'schedule': crontab(minute='*/2'),
    },
}

# Logging settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s: %(levelname)s/%(name)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', ]
    },
    'loggers': {
        'django': {
            'propagate': True,
        },
    }
}
