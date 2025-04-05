from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    """菜单模型"""
    name = models.CharField(
        max_length=50,
        verbose_name='菜单名称'
    )
    path = models.CharField(
        max_length=100,
        verbose_name='菜单路径'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='菜单图标'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父菜单'
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name='排序'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用'
    )
    permission_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='权限代码'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class UserMenu(models.Model):
    """用户菜单权限"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='menu_permissions',
        verbose_name='用户'
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='user_permissions',
        verbose_name='菜单'
    )
    has_permission = models.BooleanField(
        default=True,
        verbose_name='是否有权限'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        verbose_name = '用户菜单权限'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'menu')

    def __str__(self):
        permission_status = '有权限' if self.has_permission else '无权限'
        return f"{self.user.username} - {self.menu.name} - {permission_status}"