import environs
import logging
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
env = environs.Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://f40d2b48920cc45890b84a61dafa83d0.serveo.net",
    "http://alfaopros.fun",
    "https://alfaopros.fun",
    "http://insncby.fun",
    "https://insncby.fun",
    "http://oprosbyn.space",
    "https://oprosbyn.space",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Modules
    'blacklist',
    # Apps
    'web_site',
    'bot'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'blacklist.middleware.BlacklistMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Locale
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

# Blacklist
DEFAULT_BLOCK_TIME = 31536000  # 365 days
BLACKLIST_ADDRESS_SOURCE = env.str("BLACKLIST_ADDRESS_SOURCE")  # HTTP_X_FORWARDED_FOR

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': "%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s",
        }
    },
    'handlers': {
        'handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': 'log.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        }
    },
    'loggers': {
        'web_site': {
            'level': 'INFO',
            'handlers': ['handler'],
            'propagate': False,
        },
        'bot': {
            'level': 'INFO',
            'handlers': ['handler'],
            'propagate': False,
        }
    }
}