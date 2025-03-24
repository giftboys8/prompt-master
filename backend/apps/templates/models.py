from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class TemplateTest(models.Model):
    MODEL_CHOICES = [
        ('GPT-3.5', 'GPT-3.5'),
        ('GPT-4', 'GPT-4'),
        ('CLAUDE', 'Claude'),
        # 添加其他模型选项
    ]

    template = models.ForeignKey(
        'Template',
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='测试模板'
    )
    model = models.CharField('测试模型', max_length=20, choices=MODEL_CHOICES)
    input_data = models.JSONField('输入数据')
    output_content = models.TextField('输出内容')
    prompt = models.TextField('生成的提示词', blank=True, null=True)
    dify_response = models.JSONField('Dify API响应', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='template_tests',
        verbose_name='创建者'
    )

    class Meta:
        verbose_name = '模板测试'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.template.name} - {self.model} Test'

class Template(models.Model):
    VISIBILITY_CHOICES = [
        ('PRIVATE', '私有'),
        ('PUBLIC', '公开'),
        ('SHARED', '共享'),
    ]
    
    @classmethod
    def get_framework_type_choices(cls):
        """动态获取框架类型选项"""
        from frameworks.models import Framework
        frameworks = Framework.objects.values_list('name', 'name')
        choices = list(frameworks)
        choices.append(('CUSTOM', '自定义'))  # 保留自定义选项
        return choices
    
    name = models.CharField('模板名称', max_length=100)
    framework_type = models.CharField(
        '框架类型',
        max_length=100,  # 增加长度以适应更长的框架名称
        choices=[],  # 初始为空，将在运行时动态填充
        null=False,
        blank=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('framework_type').choices = self.get_framework_type_choices()
    framework = models.ForeignKey(
        'frameworks.Framework',
        on_delete=models.PROTECT,
        related_name='templates',
        verbose_name='框架',
        null=False,
        blank=False
    )
    visibility = models.CharField(
        '可见性',
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PRIVATE'
    )
    description = models.TextField('描述')
    content = models.JSONField('内容')
    variables = models.JSONField('变量', default=list)
    order = models.IntegerField('排序', default=0)
    target_role = models.CharField('适用角色', max_length=100, blank=True, null=True)
    
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
        ordering = ['order', '-created_at']

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
            framework=self.framework,
            framework_type=self.framework_type,
            content=self.content,
            variables=self.variables,
            target_role=self.target_role,
            created_by=self.created_by
        )

class SharedTemplate(models.Model):
    """模板分享记录"""
    STATUS_CHOICES = [
        ('PENDING', '待处理'),
        ('ACCEPTED', '已接受'),
        ('REJECTED', '已拒绝'),
    ]
    
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='shares',
        verbose_name='模板'
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_with_me',
        verbose_name='被分享用户'
    )
    can_edit = models.BooleanField('可编辑', default=False)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_templates',
        verbose_name='创建者'
    )

    class Meta:
        verbose_name = '共享模板'
        verbose_name_plural = verbose_name
        unique_together = [('template', 'shared_with')]

    def __str__(self):
        return f'{self.template.name} shared with {self.shared_with.username}'


class TemplateVersion(models.Model):
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='模板'
    )
    version_number = models.IntegerField('版本号')
    name = models.CharField('模板名称', max_length=100)
    framework = models.ForeignKey(
        'frameworks.Framework',
        on_delete=models.PROTECT,
        related_name='template_versions',
        verbose_name='框架',
        null=True,
        blank=True
    )
    framework_type = models.CharField(
        '框架类型',
        max_length=100,
        choices=[],  # 初始为空，将在运行时动态填充
        default='CUSTOM'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('framework_type').choices = Template.get_framework_type_choices()
    description = models.TextField('描述')
    content = models.JSONField('内容')
    variables = models.JSONField('变量', default=list)
    target_role = models.CharField('适用角色', max_length=100, blank=True, null=True)
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
        template.framework = self.framework
        template.description = self.description
        template.content = self.content
        template.variables = self.variables
        template.save()