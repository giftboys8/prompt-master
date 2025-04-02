from django.db import models
from django.conf import settings
import json

# 检查数据库引擎，为不同数据库提供兼容性
if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    from django.contrib.postgres.fields import ArrayField
else:
    # 为SQLite等其他数据库创建一个ArrayField模拟类
    class ArrayField(models.TextField):
        def __init__(self, base_field, **kwargs):
            self.base_field = base_field
            super().__init__(**kwargs)
        
        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs['base_field'] = self.base_field
            return name, path, args, kwargs
        
        def from_db_value(self, value, expression, connection):
            if value is None:
                return value
            return json.loads(value)
        
        def to_python(self, value):
            """确保返回标准的字符串数组格式"""
            if value is None:
                return []
                
            # 如果已经是列表，确保每个元素都是字符串
            if isinstance(value, list):
                result = []
                for item in value:
                    if isinstance(item, list) and len(item) > 0:
                        # 处理嵌套列表，取第一个元素
                        result.append(str(item[0]))
                    elif item is not None and str(item).strip():
                        # 过滤掉None和空字符串
                        result.append(str(item).strip())
                return result
                
            # 处理字符串形式的JSON数组
            if isinstance(value, str):
                if value.startswith('[') and value.endswith(']'):
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list):
                            # 递归调用自身处理解析后的列表
                            return self.to_python(parsed)
                        else:
                            # 非列表类型的JSON，作为单个元素
                            return [str(parsed)]
                    except json.JSONDecodeError:
                        # 解析失败，作为单个元素
                        return [value] if value.strip() else []
                # 普通字符串作为单个元素
                return [value] if value.strip() else []
                
            # 其他类型转为字符串作为单个元素
            return [str(value)]
        
        def get_prep_value(self, value):
            """在保存到数据库前标准化数组格式"""
            if value is None:
                return json.dumps([])
                
            # 确保value是列表
            if not isinstance(value, list):
                if isinstance(value, str):
                    if value.startswith('[') and value.endswith(']'):
                        try:
                            value = json.loads(value)
                        except json.JSONDecodeError:
                            value = [value]
                    else:
                        value = [value]
                else:
                    value = [str(value)]
            
            # 标准化列表中的每个元素
            normalized = []
            for item in value:
                if isinstance(item, list) and len(item) > 0:
                    normalized.append(str(item[0]))
                elif item is not None and str(item).strip():
                    normalized.append(str(item).strip())
            
            # 移除重复项
            normalized = list(dict.fromkeys(normalized))
            
            return json.dumps(normalized)


class Scene(models.Model):
    """场景基础信息表"""
    name = models.CharField(max_length=100, verbose_name="场景名称")
    category = models.CharField(max_length=50, verbose_name="场景分类")
    description = models.TextField(verbose_name="场景描述")
    target_roles = ArrayField(
        models.CharField(max_length=50),
        verbose_name="目标角色"
    )
    status = models.BooleanField(default=True, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="创建者"
    )
    version = models.CharField(max_length=20, verbose_name="版本号")

    class Meta:
        verbose_name = "场景"
        verbose_name_plural = "场景"
        db_table = "scenes"
        indexes = [
            models.Index(fields=['name', 'category', 'status']),
        ]

    def __str__(self):
        return self.name


class SceneTask(models.Model):
    """场景任务表"""
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="所属场景"
    )
    name = models.CharField(max_length=100, verbose_name="任务名称")
    description = models.TextField(verbose_name="任务描述")
    template = models.ForeignKey(
        'templates.Template',
        on_delete=models.CASCADE,
        verbose_name="关联模板",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "场景任务"
        verbose_name_plural = "场景任务"
        db_table = "scene_tasks"

    def __str__(self):
        return f"{self.scene.name} - {self.name}"


class SceneTemplate(models.Model):
    """场景模版关联表"""
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='templates',
        verbose_name="所属场景"
    )
    template = models.ForeignKey(
        'templates.Template',
        on_delete=models.CASCADE,
        verbose_name="关联模版"
    )
    priority = models.IntegerField(default=0, verbose_name="优先级")
    parameters = models.JSONField(null=True, blank=True, verbose_name="参数配置")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "场景模版关联"
        verbose_name_plural = "场景模版关联"
        db_table = "scene_templates"
        ordering = ['priority']

    def __str__(self):
        return f"{self.scene.name} - {self.template.name}"


class SceneVersion(models.Model):
    """场景版本历史表"""
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name="所属场景"
    )
    version_number = models.CharField(max_length=20, verbose_name="版本号")
    description = models.TextField(null=True, blank=True, verbose_name="版本描述")
    content = models.JSONField(verbose_name="版本内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="创建者"
    )

    class Meta:
        verbose_name = "场景版本"
        verbose_name_plural = "场景版本"
        db_table = "scene_versions"

    def __str__(self):
        return f"{self.scene.name} - {self.version_number}"


class SceneUsage(models.Model):
    """场景使用统计表"""
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='usages',
        verbose_name="所属场景"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="使用者"
    )
    template = models.ForeignKey(
        'templates.Template',
        on_delete=models.CASCADE,
        verbose_name="使用模版"
    )
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="使用时间")
    feedback_score = models.IntegerField(null=True, blank=True, verbose_name="反馈评分")
    feedback_content = models.TextField(null=True, blank=True, verbose_name="反馈内容")

    class Meta:
        verbose_name = "场景使用统计"
        verbose_name_plural = "场景使用统计"
        db_table = "scene_usage"

    def __str__(self):
        return f"{self.scene.name} - {self.user.username}"