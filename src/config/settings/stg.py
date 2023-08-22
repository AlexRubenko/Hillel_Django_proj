from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = "django-insecure-*5lco_em7k3!fq2phjb613m%df=4ewzzqz5km4le0lk2c50p_6"

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3", # NOQA
    }
}

STATIC_URL = "static/"
