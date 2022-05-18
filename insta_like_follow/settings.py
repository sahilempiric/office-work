"""
Django settings for insta_like_follow project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
# import firebase_admin
#from firebase_admin import firebase_init

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APP_LOG_FILENAME = os.path.join(BASE_DIR, 'log/app.log')
ERROR_LOG_FILENAME = os.path.join(BASE_DIR, 'log/error.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': APP_LOG_FILENAME
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console','file'],
        },
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n@1$7qrta@!=zb!yb!zk*2)9%us3=+)c)k8n&2cw7dr8ydnmw7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['.freelikesandfollowers.com', '143.198.184.59', "*"]


# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'INSTA_ALL',
    # 'fcm_django',
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

ROOT_URLCONF = 'insta_like_follow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'insta_like_follow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'instalikedb',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': 'localhost',    
        'PORT' : '',
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'instalikedb',
#             'USER': 'python',
#             'PASSWORD': '0000',
#             'HOST': 'localhost',    
#             'PORT' : '5432',
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_AGE = 900
SESSION_SAVE_EVERY_REQUEST = True

# Changeble
APP_URL = '/root/insta_like_follow/'


# CRONJOBS = [
#     ('*/2 * * * *', 'myapp.cron.my_cron_job')
# ]
# CRONJOBS = [
#     ('0 */1 * * *', 'INSTA_ALL.cron.getRefreshToken'),
# ]
CRONJOBS = [
   ('0 */1 * * *', 'INSTA_ALL.cron.getRefreshToken'),
    ('*/1 * * * *', 'INSTA_ALL.cron.offer_check'),
    ('0 5 * * *', 'INSTA_ALL.cron.dailynotify'),
    ('0 9 * * *', 'INSTA_ALL.cron.offer_notify'),   
    ('0 0 */1 * *', 'INSTA_ALL.cron.user_order_del'),    
]


#FIREBASE_APP = firebase_admin.initialize_app()
# FCM_DJANGO_SETTINGS = {
#      # default: _('FCM Django')
#     "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
#      # true if you want to have only one active device per registered user at a time
#      # default: False
#     #"ONE_DEVICE_PER_USER": True/False,
#     "ONE_DEVICE_PER_USER": False,
#      # devices to which notifications cannot be sent,
#      # are deleted upon receiving error response from FCM
#      # default: False
#     #"DELETE_INACTIVE_DEVICES": True/False,
#     "DELETE_INACTIVE_DEVICES": False,
# }
