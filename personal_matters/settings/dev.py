from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%rv5)#iik1z392kid5qeyjtyd)&3j#*jycjah&*7$(w%-*$&1i"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:

    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

    DEBUG = True

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    __base_path__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __log_path__ = os.path.join(__base_path__, "log")

    if not os.path.exists(__log_path__):
        os.makedirs(__log_path__)
    from datetime import datetime

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{levelname}][{asctime}][{module}][{process:d}][{thread:d}][{message}]",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                'formatter': 'verbose',
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(__log_path__, 
                                         f"django_logfile_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')[:23]}.log"),
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }


