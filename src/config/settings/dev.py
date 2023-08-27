from config.settings.base import *  # NOQA
import dj_database_url


DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS = []

url = "postgres://vuyxnphi:Ri5klwnxNX4NRYwV9etHpaqKut3XvHm2@trumpet.db.elephantsql.com/vuyxnphi"
db_config = dj_database_url.parse(url)

DATABASES = {
    "default": db_config
}

STATIC_URL = "static/"
