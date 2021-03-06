"""
Django settings for swe0 project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', ')m2y-(#as&1vb6+^g!w(^%mhh#@5x1)dc7lpb6@#_drcv$ac7)')

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
    'guardian',
    'social_django',
    'swe0.accounts',
    'swe0.core',
    'swe0.events',
    'swe0.polls',
    'swe0.profiles',
    'swe0.slack',
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

ROOT_URLCONF = 'swe0.urls'

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

WSGI_APPLICATION = 'swe0.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Override by specifying the DATABASE_URL environment variable.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{}'.format(os.path.join(BASE_DIR, '..', 'db.sqlite3')),
    ),
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

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:log-in'
LOGIN_REDIRECT_URL = 'core:home'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.slack.SlackOAuth2',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_SLACK_KEY = os.getenv('SLACK_CLIENT_ID')
SOCIAL_AUTH_SLACK_SECRET = os.getenv('SLACK_CLIENT_SECRET')

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'swe0.accounts.pipelines.create_user_if_allowed',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'swe0.accounts.pipelines.populate_user_name',
    'social_core.pipeline.user.user_details',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.getenv('STATIC_ROOT')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '..', 'static')]


MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'


# If provided, only users whose email address domain is included here
# will be able to create their own user accounts.
SWE0_CREATE_USER_WHITELISTED_DOMAINS = ['buffalo.edu']


# API token for making requests to Slack.
SWE0_SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')

# Used to verify requests from Slack
# See https://api.slack.com/docs/verifying-requests-from-slack
SWE0_SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


GUARDIAN_MONKEY_PATCH = False
