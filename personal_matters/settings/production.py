from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pg_sql_db_name",
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': "ipaddress",
        'PORT': "5432",
    }
}
