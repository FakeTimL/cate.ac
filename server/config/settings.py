"""
Django settings for drp49 project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = os.environ['DRP49_SECRET_KEY']
DEBUG = (os.environ.get('DRP49_DEBUG', '') == '1')
ALLOWED_HOSTS = ['localhost'] + (['*'] if DEBUG else os.environ.get('DRP49_ALLOWED_HOSTS', '').split())

# Application definition
INSTALLED_APPS = [
  'main.apps.MainConfig',
  'accounts.apps.AccountsConfig',
  'rest_framework',  # The django REST framework
  'django.contrib.staticfiles',  # Static files system
  'django.contrib.contenttypes',  # Relations between models (used in permissions system)
  'django.contrib.sessions',  # User session system
  'django.contrib.auth',  # User authentication system
  'django.contrib.messages',  # One-time messages
  'django.contrib.admin',  # Administration site
  'django.contrib.humanize',  # Additional templates
]
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',  # Security
  "whitenoise.middleware.WhiteNoiseMiddleware",  # Temporary static files server
  'django.contrib.sessions.middleware.SessionMiddleware',  # User session system
  'django.middleware.locale.LocaleMiddleware',  # Localization, datetime format
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',  # Security: csrf protection
  'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication system
  'django.contrib.messages.middleware.MessageMiddleware',  # One-time messages
  'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Security: clickjacking protection
]
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      BASE_DIR / 'templates',  # Global template directories
      BASE_DIR.parent / 'client' / 'dist'
    ],
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
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': 'localhost',
    'PORT': '3306',
    'USER': os.environ['DRP49_MYSQL_USERNAME'],
    'PASSWORD': os.environ['DRP49_MYSQL_PASSWORD'],
    'NAME': os.environ['DRP49_MYSQL_DB_NAME'],
    'OPTIONS': {
      'init_command': " \
        SET sql_mode='STRICT_TRANS_TABLES', \
        default_storage_engine=INNODB, \
        character_set_connection=utf8mb4, \
        collation_connection=utf8mb4_unicode_520_ci; \
      ",
      'charset': 'utf8mb4',
    },
  }
}

# Custom authentication
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
AUTHENTICATION_BACKENDS = [
  'django.contrib.auth.backends.ModelBackend',  # Default backend
  # 'accounts.models.EmailAuthBackend', # Custom backend for logging in with email address
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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

# Elasticsearch
# https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html
ELASTICSEARCH_DSL = {
  'default': {
    'hosts': 'localhost:9200'
  },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# LOCALE_PATHS = [BASE_DIR / 'locale']
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = True
# USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, etc.) and user uploaded media files (images, videos, etc.)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# https://docs.djangoproject.com/en/4.2/topics/files/
STATICFILES_DIRS = [
  BASE_DIR / 'static',  # Global static file directories
  BASE_DIR.parent / 'client' / 'dist',
]

# Using WhiteNoise for static files storage
# https://whitenoise.readthedocs.io/en/latest/django.html
# Using AWS S3 for media storage
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
if DEBUG:
  STATIC_URL = '/static/'  # Static file web URL
  MEDIA_URL = '/media/'  # User-uploaded file web URL
  STATIC_ROOT = BASE_DIR / 'static_root'
  MEDIA_ROOT = BASE_DIR / 'media_root'

else:
  STATIC_URL = os.environ['DRP49_STATIC_URL']
  MEDIA_URL = os.environ['DRP49_MEDIA_URL']
  STATIC_ROOT = BASE_DIR / 'static_root'
  AWS_S3_ACCESS_KEY_ID = os.environ['DRP49_AMAZON_S3_ACCESS_KEY_ID']
  AWS_S3_SECRET_ACCESS_KEY = os.environ['DRP49_AMAZON_S3_SECRET_ACCESS_KEY']
  AWS_S3_REGION_NAME = os.environ['DRP49_AMAZON_S3_REGION']
  AWS_STORAGE_BUCKET_NAME = os.environ['DRP49_AMAZON_S3_BUCKET']
  AWS_LOCATION = os.environ.get('DRP49_AMAZON_S3_LOCATION', default='')
  STORAGES = {
    "staticfiles": {
      "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
      "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
  }

# HTTP SSL configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#secure-ssl-redirect
# if not DEBUG:
#   SECURE_SSL_REDIRECT = True
#   SESSION_COOKIE_SECURE = True
#   CSRF_COOKIE_SECURE = True
#   SECURE_HSTS_SECONDS = 3600

# In the presence of a reverse proxy:
# https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER
if not DEBUG:
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
# https://docs.djangoproject.com/en/4.2/topics/logging/
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'loggers': {
    'django': {
      'level': 'INFO',
      'handlers': ['file'],
      'propagate': True,
    },
  },
  'handlers': {
    'file': {
      'level': 'INFO',
      'class': 'logging.FileHandler',
      'filename': os.environ.get('DRP49_DJANGO_LOG_FILE', 'django.log'),
    },
  },
}