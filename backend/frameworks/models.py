from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Framework(models.Model):
    """Framework model for template frameworks like RTGO"""
    name = models.CharField(_('Framework Name'), max_length=100, unique=True)
    description = models.TextField(_('Framework Description'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Created By'),
        related_name='created_frameworks'
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Framework')
        verbose_name_plural = _('Frameworks')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class FrameworkModule(models.Model):
    """Module within a framework"""
    framework = models.ForeignKey(
        Framework,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name=_('Framework')
    )
    name = models.CharField(_('Module Name'), max_length=100)
    description = models.TextField(_('Module Description'))
    order = models.IntegerField(_('Display Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Framework Module')
        verbose_name_plural = _('Framework Modules')
        ordering = ['framework', 'order', 'created_at']
        unique_together = ['framework', 'name']

    def __str__(self):
        return f"{self.framework.name} - {self.name}"