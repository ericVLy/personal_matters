from .base import *

# DEBUG = False


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "" from .local


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    DEBUG = True
    
    SECRET_KEY = "django-insecure-%rv5)#iik1z392kid5qeyjtyd)&3j#*jycjah&*7$(w%-*$&1i"


    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "personal_matters",
            'USER': 'personal_matters',
            'PASSWORD': 'pm.pgarch',
            'HOST': "localhost",
            'PORT': "5432",
        }
    }
