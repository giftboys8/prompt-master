from rest_framework import serializers
from .models import Scene, SceneTask, SceneVersion, SceneUsage
from apps.templates.models import Template


class SceneTaskSerializer(serializers.ModelSerializer):
    """场景任务序列化器"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_description = serializers.CharField(source='template.description', read_only=True)

    class Meta:
        model = SceneTask
        fields = ['id', 'name', 'description', 'template',
                 'template_name', 'template_description', 'created_at']
        read_only_fields = ['id', 'created_at', 'template_name', 'template_description']


class SceneVersionSerializer(serializers.ModelSerializer):
    """场景版本历史序列化器"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = SceneVersion
        fields = ['id', 'version_number', 'description', 'content', 
                  'created_at', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_at', 'created_by_username']


class SceneUsageSerializer(serializers.ModelSerializer):
    """场景使用统计序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = SceneUsage
        fields = ['id', 'user', 'user_username', 'template', 'template_name',
                  'used_at', 'feedback_score', 'feedback_content']
        read_only_fields = ['id', 'used_at', 'user_username', 'template_name']


class SceneListSerializer(serializers.ModelSerializer):
    """场景列表序列化器"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Scene
        fields = ['id', 'name', 'category', 'description', 'target_roles', 
                  'status', 'version', 'created_at', 'updated_at', 
                  'created_by', 'created_by_username', 'tasks_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 
                           'created_by_username', 'tasks_count', 'templates_count']
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()
    


class SceneDetailSerializer(serializers.ModelSerializer):
    """场景详情序列化器"""
    tasks = SceneTaskSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Scene
        fields = ['id', 'name', 'category', 'description', 'target_roles', 
                  'status', 'version', 'created_at', 'updated_at', 
                  'created_by', 'created_by_username', 'tasks']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username']


class SceneCreateUpdateSerializer(serializers.ModelSerializer):
    """场景创建和更新序列化器"""
    tasks = SceneTaskSerializer(many=True, required=False)
    target_roles = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list
    )
    
    class Meta:
        model = Scene
        fields = ['id', 'name', 'category', 'description', 'target_roles', 
                  'status', 'version', 'tasks']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        
        # 确保target_roles是列表类型
        if 'target_roles' in validated_data and not isinstance(validated_data['target_roles'], list):
            validated_data['target_roles'] = [validated_data['target_roles']]
        
        # 创建场景
        scene = Scene.objects.create(**validated_data)
        
        # 创建任务
        for task_data in tasks_data:
            # 处理template字段
            template = task_data.pop('template', None)
            if template:
                # 如果template是一个对象，获取其ID
                template_id = template.id if hasattr(template, 'id') else template
                from apps.templates.models import Template
                try:
                    template_obj = Template.objects.get(id=template_id)
                    SceneTask.objects.create(scene=scene, template=template_obj, **task_data)
                except Template.DoesNotExist:
                    pass
            else:
                SceneTask.objects.create(scene=scene, **task_data)
        
        # 创建初始版本
        SceneVersion.objects.create(
            scene=scene,
            version_number=scene.version,
            content={
                'scene': {
                    'name': scene.name,
                    'category': scene.category,
                    'description': scene.description,
                    'target_roles': scene.target_roles,
                    'status': scene.status,
                },
                'tasks': tasks_data
            },
            created_by=scene.created_by
        )
        
        return scene
    
    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        
        # 确保target_roles是列表类型且每个元素都是字符串
        if 'target_roles' in validated_data:
            if not isinstance(validated_data['target_roles'], list):
                validated_data['target_roles'] = [str(validated_data['target_roles'])]
            else:
                validated_data['target_roles'] = [str(role) for role in validated_data['target_roles'] if role]
        
        # 更新场景基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 如果提供了任务数据，更新任务
        if tasks_data is not None:
            # 删除现有任务
            instance.tasks.all().delete()
            
            # 创建新任务
            for task_data in tasks_data:
                SceneTask.objects.create(scene=instance, **task_data)
        
        return instance