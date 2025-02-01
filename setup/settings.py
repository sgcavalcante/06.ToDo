"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path

from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR ,"media/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-#!4-!%+lvrnh#$*7aq(u%6&xta9w0cx-5e3%x%t6=-3k_u3s!c'
SECRET_KEY = str(os.getenv('CHAVE_SECRETA'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['s6c.up.railway.app','www.ventosolares.com.br','web-production-f8f8d.up.railway.app','sanicousintario.up.railway.app','127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://web-production-f8f8d.up.railway.app','https://s6c.up.railway.app','https://sanicousintario.up.railway.app','https://www.ventosolares.com.br']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
     
    'dpd_static_support',
    'channels',
    'rest_framework',  # Adicione esta linha
    'apps.to_do',
]

ASGI_APPLICATION = 'myproject.asgi.application'  # Substitua 'myproject' pelo nome do seu projeto


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',  # Middleware necessário
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',  # Middleware necessário
]


ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL")
#DATABASES = {'default': dj_database_url.config(default=DATABASE_URL,conn_max_age=20)}


PGHOST=os.getenv("PGHOST")          # monorail.proxy.rlwy.net
PGUSER=os.getenv("PGUSER")          # postgres
PGPASSWORD=os.getenv("PGPASSWORD")  # ErflndgNadXEJEwnVEeaLXvpdpZfmEQW
PGDATABASE=os.getenv("PGDATABASE")  # railway
PGPORT=os.getenv("PORT")            # 29466

#ssads
#teste

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv(PGDATABASE),
        'USER': os.getenv(PGUSER),
        'PASSWORD': os.getenv(PGPASSWORD),
        'HOST': os.getenv(PGHOST),
        'PORT': os.getenv(PGPORT),#, '5432'),
    }
}





# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

 

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIR = [os.path.join(BASE_DIR,'static'),]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configurações do Django Plotly Dash
X_FRAME_OPTIONS = 'SAMEORIGIN'
PLOTLY_DASH = {
    'ws_route': 'dpd/ws/channel',  # WebSocket route
    'http_route': 'dpd/views',  # HTTP route
    'insert_demo_migrations': True,
}