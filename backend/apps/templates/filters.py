from django_filters import rest_framework as filters
from .models import Template
import json

class TemplateFilter(filters.FilterSet):
    target_role = filters.CharFilter(method='filter_target_role')

    def filter_target_role(self, queryset, name, value):
        if not value:
            return queryset
            
        try:
            # 检查 target_role 是否为 null
            base_queryset = queryset.exclude(target_role__isnull=True)
            
            # 如果没有任何记录有 target_role，返回空查询集
            if not base_queryset.exists():
                return queryset.none()
            
            # 在 Python 层面处理过滤
            filtered_ids = []
            for template in base_queryset:
                try:
                    target_roles = template.target_role
                    
                    # 如果是字符串，尝试解析为 JSON
                    if isinstance(target_roles, str):
                        try:
                            target_roles = json.loads(target_roles)
                        except json.JSONDecodeError:
                            # 如果解析失败，将其视为单个角色
                            target_roles = [target_roles]
                    
                    # 如果不是列表，转换为列表
                    if not isinstance(target_roles, list):
                        target_roles = [target_roles]
                    
                    # 将所有角色转换为字符串并解码 Unicode
                    decoded_roles = []
                    for role in target_roles:
                        if role:
                            if isinstance(role, str):
                                try:
                                    # 尝试解码 Unicode 转义序列
                                    decoded_role = role.encode().decode('unicode-escape')
                                except UnicodeError:
                                    decoded_role = role
                            else:
                                decoded_role = str(role)
                            decoded_roles.append(decoded_role)
                    
                    # 检查搜索值是否匹配任何解码后的角色
                    if any(value.lower() in decoded_role.lower() for decoded_role in decoded_roles):
                        filtered_ids.append(template.id)
                        
                except Exception as template_error:
                    print(f"处理模板 {template.id} 的目标角色时出错: {template_error}")
                    continue
            
            # 如果没有匹配的记录，返回空查询集
            if not filtered_ids:
                return queryset.none()
            
            return queryset.filter(id__in=filtered_ids)
        except Exception as e:
            print(f"过滤器错误: {e}")
            return queryset.none()

    class Meta:
        model = Template
        fields = ['framework', 'visibility', 'target_role']