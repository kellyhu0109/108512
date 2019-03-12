"""
Django settings for medicine_resort_bot project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


try:
    from .settings_secret import *
except ImportError:
    SECRET_KEY = get_env_variable('9ee*!)y3=#7_s1&0=*!l-+q#9f#2_d*fsh$osh3md)j3__kkiq')
    LINE_CHANNEL_ACCESS_TOKEN = get_env_variable('m2Q7OLhF/Wk1+QL2YnKnnzGS9X+A5vKLonIYE4fieNlsrp1KxoQIscAxp90UwJONCVmWayFjUwMGjts9jDgkmW/Jcblgu6FPjBtzBpILYcoxWzezrBksvQ239bEyYbh0WOsK6YILTLlN/Ss4ETJ2HwdB04t89/1O/w1cDnyilFU=')
    LINE_CHANNEL_SECRET = get_env_variable('5c4c2c80c935db38cbbf0eefcf58c27b')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9ee*!)y3=#7_s1&0=*!l-+q#9f#2_d*fsh$osh3md)j3__kkiq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medicine_resort_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'medicine_resort_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# LINE_CHANNEL_ACCESS_TOKEN = "BJxAW23mibhsRVOzGf97jDSguH17tEHKmrtC8Y/LteMsgKEahMEaQdDcod/kJQl/ql6BGjWvu/VONvS91kcQ6SKUaos2ZbQCBffI9MyOi9LRHJi9DAXEM9sJhLqmX0G+Nq9vh2rbH0iqbJ36pFLwywdB04t89/1O/w1cDnyilFU="
# LINE_CHANNEL_SECRET = "8dc71d55d0ba3b4a060ea51cfcc5b939"