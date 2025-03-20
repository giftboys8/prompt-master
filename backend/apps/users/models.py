from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户'
    )
    phone = models.CharField(
        max_length=11,
        blank=True,
        verbose_name='手机号'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='头像'
    )

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的个人信息"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建用户信息"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时自动保存用户信息"""
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()