from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# 在开发环境中禁用CSRF
CSRF_TRUSTED_ORIGINS = ['http://localhost:5173']
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# CORS配置
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境允许所有源
CORS_ALLOW_CREDENTIALS = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prompt_master_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}