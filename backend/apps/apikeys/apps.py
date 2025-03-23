from django.apps import AppConfig


class ApikeysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.apikeys'
    label = 'apikeys'
    verbose_name = 'API秘钥管理'