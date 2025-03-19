from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """扩展用户模型"""
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    avatar = models.URLField(max_length=200, blank=True, verbose_name='头像URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username