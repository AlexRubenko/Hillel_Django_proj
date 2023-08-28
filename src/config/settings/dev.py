from config.settings.base import *  # NOQA
import dj_database_url


DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS = []

url = "postgres://juvdcpov:9AvNuu4Iw_mLt8B4LSx3IYl2V_OzJeZD@trumpet.db.elephantsql.com/juvdcpov"
db_config = dj_database_url.parse(url)

DATABASES = {
    "default": db_config
}

STATIC_URL = "static/"
