from rest_framework import serializers
from .models import Framework, FrameworkModule


class FrameworkModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameworkModule
        fields = ['id', 'name', 'description', 'order', 'created_at', 'updated_at']


class FrameworkSerializer(serializers.ModelSerializer):
    modules = FrameworkModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Framework
        fields = ['id', 'name', 'description', 'modules', 'created_at', 'updated_at']


class FrameworkCreateSerializer(serializers.ModelSerializer):
    modules = FrameworkModuleSerializer(many=True, required=False)
    
    class Meta:
        model = Framework
        fields = ['id', 'name', 'description', 'modules']
    
    def create(self, validated_data):
        modules_data = validated_data.pop('modules', [])
        framework = Framework.objects.create(**validated_data)
        
        for module_data in modules_data:
            FrameworkModule.objects.create(framework=framework, **module_data)
        
        return framework
    
    def update(self, instance, validated_data):
        modules_data = validated_data.pop('modules', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Handle modules update logic here if needed
        # This is simplified; you might want to implement a more sophisticated
        # update logic for modules in a real application
        
        return instance