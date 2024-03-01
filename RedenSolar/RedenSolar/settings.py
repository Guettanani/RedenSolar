import os
from pathlib import Path
import os
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True  # Assurez-vous que DEBUG est désactivé en production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e=y-5=d*@)wlu9y@+v$ue1*vkam5cp3)3zp%asr&9&8ytvva(-'

# Configurez CORS pour autoriser les requêtes provenant de http://localhost:8050/
CORS_ALLOWED_ORIGINS = [
    "https://icamapp.reden.cloud",
    "https://webicamapp.reden.cloud",
    "http://localhost"
]

ALLOWED_HOSTS = ['webicamapp.reden.cloud', 'localhost']

ENABLE_SECURE_PROXY_SSL_HEADER = os.environ.get("ENABLE_SSL", False)
if ENABLE_SECURE_PROXY_SSL_HEADER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_PROXY_SSL_HEADER = None

CSRF_TRUSTED_ORIGINS = ['https://icamapp.reden.cloud','https://webicamapp.reden.cloud','http://localhost/']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'corsheaders',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'django_celery_beat',
    'django_crontab',
    'rest_framework'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'RedenSolar.urls'

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

WSGI_APPLICATION = 'RedenSolar.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configurez votre base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db',
        'USER': 'postgres',
        'PASSWORD': 'reden12345',
        'HOST':  '172.25.0.2', #  Hostname of the database service
        'PORT': '5432',
        'OPTIONS': {
            'options': f'-c timezone={TIME_ZONE}',
        },
    }
}





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





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT= '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", 'redis://redis:6379/0')
CELERY_TIMEZONE = 'Europe/Paris'

CELERY_BEAT_SCHEDULE = {
    'scheduled_task': {
        'task': 'Envoi des données dynamiques d\'Energysoft dans la base de données',
        'schedule': crontab(month_of_year='*', day_of_month='*', day_of_week='*', hour=15, minute=15),
    },
}

CELERY_CACHE_BACKEND = 'default'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cachedb',
    }
}
