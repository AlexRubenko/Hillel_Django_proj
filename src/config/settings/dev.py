from config.settings.base import *  # NOQA

DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'document_flow',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_URL = "static/"
