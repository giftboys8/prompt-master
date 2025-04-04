from django_filters import rest_framework as filters
from .models import Template
import json

class TemplateFilter(filters.FilterSet):
    target_role = filters.CharFilter(method='filter_target_role')

    def filter_target_role(self, queryset, name, value):
        """
        过滤适用角色。
        由于target_role是JSONField，我们需要在Python层面进行过滤。
        """
        if not value:
            return queryset
        
        try:
            # 尝试解析JSON数组
            roles = json.loads(value)
            if isinstance(roles, list):
                # 如果是列表，我们需要检查任何一个角色是否匹配
                return queryset.filter(id__in=[
                    template.id for template in queryset
                    if any(role in template.target_role for role in roles)
                ])
            else:
                # 如果不是列表，就当作单个值处理
                return queryset.filter(id__in=[
                    template.id for template in queryset
                    if roles in template.target_role
                ])
        except json.JSONDecodeError:
            # 如果不是有效的JSON，就当作单个字符串处理
            # 移除可能的方括号
            value = value.strip('[]').replace('"', '').strip()
            return queryset.filter(id__in=[
                template.id for template in queryset
                if value in template.target_role
            ])

    class Meta:
        model = Template
        fields = ['framework', 'visibility', 'target_role']