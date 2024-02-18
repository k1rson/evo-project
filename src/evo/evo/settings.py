import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-$hme!($7oxy#kl1la-xd=@&d@90&%u!_exm*z(5q%da_&d683!'

DEBUG = True

ALLOWED_HOSTS = ['*']
ASGI_APPLICATION = 'evo.asgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'rest_framework.authtoken',
    'channels',
    'apps.authentication_app.apps.AuthenticationAppConfig',
    'apps.mail_client_app.apps.MailClientAppConfig', 
    'apps.main_app.apps.MainAppConfig', 
    'apps.chat_app.apps.ChatAppConfig'
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

ROOT_URLCONF = 'evo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('', 'templates')],
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

WSGI_APPLICATION = 'evo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'evo-db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'authentication_app.CustomUser'

# STATIC FILES CONFIGURATION
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'shared_static',
]

# MEDIA FILES CONFIGURATION
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DRF CONFIG
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ], 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# DJANGO CHANNELS CONFIG
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Используйте это для разработки
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',  # Используйте это для боевого использования
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],  # Настройте соединение с вашим Redis-сервером
        # },
    },
}

# EMAIL CONFING

# IMAP CONFIGURATION
IMAP_SERVER = 'imap.mail.ru'
IMAP_PORT = 993
IMAP_USERNAME = 'evo-inc-sup@mail.ru'
IMAP_PASSWORD = 'KTchrGp7NM6wZg1gty5R'

# SMTP CONFIGURATION
SMTP_SERVER = 'smtp.mail.ru'
SMTP_PORT = 465 
SMTP_USERNAME = 'evo-inc-sup@mail.ru'
SMTP_PASSWORD = 'KTchrGp7NM6wZg1gty5R'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'