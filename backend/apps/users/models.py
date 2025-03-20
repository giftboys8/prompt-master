from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.username