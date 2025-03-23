from django.db import models
from django.conf import settings


class ApiKey(models.Model):
    platform_name = models.CharField(max_length=100, verbose_name="平台名称")
    scene_name = models.CharField(max_length=100, verbose_name="场景名称")
    key = models.CharField(max_length=255, verbose_name="API秘钥")
    description = models.TextField(blank=True, verbose_name="描述信息")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='api_keys', verbose_name="用户")

    class Meta:
        verbose_name = "API秘钥"
        verbose_name_plural = verbose_name
        unique_together = ('platform_name', 'scene_name', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform_name} - {self.scene_name}"