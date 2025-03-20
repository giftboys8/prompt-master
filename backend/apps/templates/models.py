from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Template(models.Model):
    FRAMEWORK_CHOICES = [
        ('RTGO', 'RTGO'),
        ('SPAR', 'SPAR'),
        ('CUSTOM', 'Custom'),
    ]

    name = models.CharField('模板名称', max_length=100)
    framework_type = models.CharField('框架类型', max_length=10, choices=FRAMEWORK_CHOICES)
    description = models.TextField('描述')
    content = models.JSONField('内容')
    variables = models.JSONField('变量', default=list)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='templates',
        verbose_name='创建者'
    )

    class Meta:
        verbose_name = '提示词模板'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 保存模板时自动创建新版本
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            version_number = 1
        else:
            latest_version = self.versions.order_by('-version_number').first()
            version_number = (latest_version.version_number + 1) if latest_version else 1

        TemplateVersion.objects.create(
            template=self,
            version_number=version_number,
            name=self.name,
            framework_type=self.framework_type,
            description=self.description,
            content=self.content,
            variables=self.variables,
            created_by=self.created_by
        )

class TemplateVersion(models.Model):
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='模板'
    )
    version_number = models.PositiveIntegerField('版本号')
    name = models.CharField('模板名称', max_length=100)
    framework_type = models.CharField(
        '框架类型',
        max_length=10,
        choices=Template.FRAMEWORK_CHOICES
    )
    description = models.TextField('描述')
    content = models.JSONField('内容')
    variables = models.JSONField('变量', default=list)
    is_current = models.BooleanField('是否为当前版本', default=False)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='template_versions',
        verbose_name='创建者'
    )

    class Meta:
        verbose_name = '提示词模板版本'
        verbose_name_plural = verbose_name
        ordering = ['-version_number']
        unique_together = [('template', 'version_number')]

    def __str__(self):
        return f'{self.template.name} v{self.version_number}'

    def restore(self):
        """恢复到此版本"""
        template = self.template
        template.name = self.name
        template.framework_type = self.framework_type
        template.description = self.description
        template.content = self.content
        template.variables = self.variables
        template.save()