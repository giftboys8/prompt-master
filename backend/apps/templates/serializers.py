from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Template, TemplateVersion, TemplateTest, SharedTemplate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class SharedTemplateSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(read_only=True)
    
    class Meta:
        model = SharedTemplate
        fields = ['id', 'shared_with', 'can_edit', 'created_at']

class TemplateSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    shared_with = SharedTemplateSerializer(source='shares', many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'framework', 'framework_type', 'description',
            'content', 'variables', 'order', 'target_role', 'created_at', 
            'updated_at', 'created_by', 'is_owner', 'can_edit', 'shared_with',
            'visibility'
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
        
        # 框架类型验证已移至validate方法，通过framework对象获取
        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.created_by_id == request.user.id
        return False

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # 创建者始终可以编辑
            if obj.created_by_id == request.user.id:
                return True
            # 检查是否有编辑权限的共享
            return obj.shares.filter(shared_with=request.user, can_edit=True).exists()
        return False

    def validate(self, data):
        """
        验证数据
        """
        # 移除框架内容字段的限制，允许根据框架类型灵活变化
        return data


class TemplateVersionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TemplateVersion
        fields = [
            'id', 'template', 'version_number', 'name',
            'framework', 'description', 'content',
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
    framework_type = serializers.CharField(source='template.framework_type', read_only=True)

    class Meta:
        model = TemplateTest
        fields = [
            'id', 'template', 'template_name', 'model', 'framework_type',
            'input_data', 'output_content', 'prompt', 'dify_response',
            'created_at', 'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_by', 'created_by_username', 'output_content', 'prompt', 'dify_response', 'framework_type']

    def validate_input_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('输入数据必须是字典类型')
        
        template = self.context['view'].get_object()
        required_variables = [var['name'] for var in template.variables]
        
        for var in required_variables:
            if var not in value:
                raise serializers.ValidationError(f'缺少必要的变量：{var}')
        
        return value