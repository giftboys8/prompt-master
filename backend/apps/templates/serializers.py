from rest_framework import serializers
from .models import Template, TemplateVersion, TemplateTest

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'framework_type', 'description',
            'content', 'variables', 'order', 'target_role', 'created_at', 
            'updated_at', 'created_by'
        ]
        read_only_fields = ['created_by']

    def validate_variables(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('变量必须是列表类型')
        
        variable_names = set()
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError('变量项必须是字典类型')
            
            required_fields = ['name', 'default_value', 'description']
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f'变量必须包含{field}字段')
                if not isinstance(item[field], str):
                    raise serializers.ValidationError(f'{field}必须是字符串类型')
            
            if not item['name'].isidentifier():
                raise serializers.ValidationError('变量名称必须是有效的标识符（只能包含字母、数字和下划线，且不能以数字开头）')
            
            if item['name'] in variable_names:
                raise serializers.ValidationError('变量名称不能重复')
            variable_names.add(item['name'])
        
        return value

    def validate_content(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('内容必须是字典类型')
        
        framework_type = self.initial_data.get('framework_type')
        
        if framework_type == 'RTGO':
            required_fields = ['role', 'task', 'goal', 'output']
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f'RTGO框架必须包含{field}字段')
                if not isinstance(value[field], str):
                    raise serializers.ValidationError(f'{field}必须是字符串类型')
                if not value[field].strip():
                    raise serializers.ValidationError(f'{field}不能为空')
        
        elif framework_type == 'SPAR':
            required_fields = ['situation', 'purpose', 'action', 'result']
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f'SPAR框架必须包含{field}字段')
                if not isinstance(value[field], str):
                    raise serializers.ValidationError(f'{field}必须是字符串类型')
                if not value[field].strip():
                    raise serializers.ValidationError(f'{field}不能为空')
        
        elif framework_type == 'CUSTOM':
            if 'custom' not in value:
                raise serializers.ValidationError('自定义框架必须包含custom字段')
            if not isinstance(value['custom'], str):
                raise serializers.ValidationError('custom必须是字符串类型')
            if not value['custom'].strip():
                raise serializers.ValidationError('custom不能为空')
        
        else:
            raise serializers.ValidationError('无效的框架类型')
        
        return value

    def validate(self, data):
        """
        检查框架类型和内容是否匹配
        """
        framework_type = data.get('framework_type')
        content = data.get('content', {})
        
        if framework_type == 'RTGO':
            extra_fields = set(content.keys()) - {'role', 'task', 'goal', 'output'}
            if extra_fields:
                raise serializers.ValidationError({
                    'content': f'RTGO框架不应包含以下字段：{", ".join(extra_fields)}'
                })
        
        elif framework_type == 'SPAR':
            extra_fields = set(content.keys()) - {'situation', 'purpose', 'action', 'result'}
            if extra_fields:
                raise serializers.ValidationError({
                    'content': f'SPAR框架不应包含以下字段：{", ".join(extra_fields)}'
                })
        
        elif framework_type == 'CUSTOM':
            extra_fields = set(content.keys()) - {'custom'}
            if extra_fields:
                raise serializers.ValidationError({
                    'content': f'自定义框架不应包含以下字段：{", ".join(extra_fields)}'
                })
        
        return data


class TemplateVersionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TemplateVersion
        fields = [
            'id', 'template', 'version_number', 'name',
            'framework_type', 'description', 'content',
            'variables', 'target_role', 'is_current', 'created_at',
            'created_by', 'created_by_username'
        ]
        read_only_fields = [
            'created_by', 'created_by_username',
            'version_number', 'is_current'
        ]

class TemplateTestSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TemplateTest
        fields = [
            'id', 'template', 'template_name', 'model',
            'input_data', 'output_content', 'created_at',
            'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_by', 'created_by_username', 'output_content']

    def validate_input_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('输入数据必须是字典类型')
        
        template = self.context['view'].get_object()
        required_variables = [var['name'] for var in template.variables]
        
        for var in required_variables:
            if var not in value:
                raise serializers.ValidationError(f'缺少必要的变量：{var}')
        
        return value