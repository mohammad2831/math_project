

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from datetime import timedelta
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django-environ
env = environ.Env()

# Load environment variables from .env file at repository root if present
env_file = BASE_DIR / '.env'
if env_file.is_file():
    environ.Env.read_env(str(env_file))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default=None)
if not SECRET_KEY or not SECRET_KEY.strip():
    raise ImproperlyConfigured("The DJANGO_SECRET_KEY environment variable is required and cannot be empty.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'web.apps.WebConfig',
    'accounts.apps.AccountsConfig',
    'question.apps.QuestionConfig',
    'home.apps.HomeConfig',
    'app.apps.AppConfig',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',
    'channels',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',


     'question. gzip_middleware.GZipAPIResponseMiddleware',

]

ROOT_URLCONF = 'math_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
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

#WSGI_APPLICATION = 'math_project.wsgi.application'
ASGI_APPLICATION = 'math_project.asgi.application'

# Redis Configuration
REDIS_HOST = env('REDIS_HOST', default='localhost')
REDIS_PORT = env.int('REDIS_PORT', default=6379)
REDIS_DB = env.int('REDIS_DB', default=0)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL ='accounts.User'


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS=[
    "GET",
    "POST",
    "PUT"
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_CONTENT_ENCODING':'gzip',

    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',  # for unauthenticated users
        'user': '100/minute',   # for authenticated users
    }
    

}



JWT_BLACKLIST_CACHE_ALIAS = 'default'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=100), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 
    'ROTATE_REFRESH_TOKENS': False,  
    'BLACKLIST_AFTER_ROTATION': True,  
    'ALGORITHM': 'HS256', 
    'SIGNING_KEY': SECRET_KEY,  
    'AUTH_HEADER_TYPES': ('Bearer',),  
    
    'USER_ID_FIELD': 'phone_number',  
    
    'USER_ID_CLAIM': 'user_id',  
    'BLACKLIST_TOKEN_TYPES': ('access', 'refresh'),
    "TOKEN_OBTAIN_SERIALIZER": "accounts.serializers.MyTokenObtainPairSerializer",
}



