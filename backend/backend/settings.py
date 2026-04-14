
import dj_database_url
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-14^%^d_w52!_vdcs_ob2u&d!&ta4y3$(65$nwrtys_-#zf+se3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'corsheaders',
    
    'rest_framework',
    'rest_framework_simplejwt',
    
    
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# This will look for a DATABASE_URL environment variable
# If it doesn't find one (like on your local machine), it defaults to SQLite
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://neondb_owner:npg_gBYHq6ayO0nz@ep-dark-dawn-anpsvv04-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        ,
        conn_max_age=600,
        ssl_require=True
    )
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'



# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),  # Access token expires in 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Refresh token expires in 1 day
    'ROTATE_REFRESH_TOKENS': True,                  # Gives a new refresh token when used
    'BLACKLIST_AFTER_ROTATION': True,               # Old refresh tokens become invalid
    'UPDATE_LAST_LOGIN': True,                      # Updates the 'last_login' field in User model

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,                      # Uses your Django Secret Key
    'AUTH_HEADER_TYPES': ('Bearer',),               # Frontend must send: "Authorization: Bearer <token>"
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# 1. Use the SMTP backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Now access them using os.getenv()
#SECRET_KEY = os.getenv("SECRET_KEY")
#DEBUG = os.getenv("DEBUG") == "True"

# Email Configuration
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST= os.getenv("EMAIL_HOST")
EMAIL_PORT= os.getenv("EMAIL_PORT")
EMAIL_USE_TLS=os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_PASSWORD= os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL= os.getenv("DEFAULT_FROM_EMAIL")
