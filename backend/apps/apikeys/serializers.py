from rest_framework import serializers
from .models import ApiKey


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['id', 'platform_name', 'scene_name', 'key', 'description', 
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # 添加当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)