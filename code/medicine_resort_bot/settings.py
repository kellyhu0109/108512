"""
Django settings for medicine_resort_bot project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# import django_heroku
import pymysql
pymysql.install_as_MySQLdb()

# from django.core.exceptions import ImproperlyConfigured
# import dj_database_url

LINE_CHANNEL_ACCESS_TOKEN = "m2Q7OLhF/Wk1+QL2YnKnnzGS9X+A5vKLonIYE4fieNlsrp1KxoQIscAxp90UwJONCVmWayFjUwMGjts9jDgkmW/Jcblgu6FPjBtzBpILYcoxWzezrBksvQ239bEyYbh0WOsK6YILTLlN/Ss4ETJ2HwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "5c4c2c80c935db38cbbf0eefcf58c27b"

# LINE_CHANNEL_ACCESS_TOKEN = "NPqvqJKFwybbq3t3JJz2cjFi6alSlBBXdh2x6VNi6F/lqyxkfDkG+UfatiJS5XEYlpS6IyIx4dD7LZnolyuYZDuWNDsMY4Qwix3wioF1qMXX+faC15l1tog8DFscweGzSvmapr3RYn0uIPgf2jgb1wdB04t89/1O/w1cDnyilFU="
# LINE_CHANNEL_SECRET = "12cffe8c0b7900686cdd055cda2584d4"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9ee*!)y3=#7_s1&0=*!l-+q#9f#2_d*fsh$osh3md)j3__kkiq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '140.131.114.151', 'ab4047e2.ngrok.io']

# APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap4',
    'bot',
    'django_q',
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
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'medicine_resort_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'admin',
        'PASSWORD': 'bighitbts',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SILENCED_SYSTEM_CHECKS = ['mysql.E001']

Q_CLUSTER = { 
    'name': 'DjangORM',
    'workers': 1,
    'timeout': 1800,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
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

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
