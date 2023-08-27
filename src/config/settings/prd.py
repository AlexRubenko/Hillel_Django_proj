from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = "django-insecure-*5lco_em7k3!fq2phjb613m%df=4ewzzqz5km4le0lk2c50p_6"

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
