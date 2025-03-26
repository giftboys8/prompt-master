from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# 在开发环境中禁用CSRF
CSRF_TRUSTED_ORIGINS = ['http://localhost:5173']
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}