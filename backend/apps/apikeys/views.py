from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ApiKey
from .serializers import ApiKeySerializer


class IsOwner(permissions.BasePermission):
    """
    自定义权限：只允许对象的所有者访问
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ApiKeyViewSet(viewsets.ModelViewSet):
    """
    API秘钥管理视图集
    """
    serializer_class = ApiKeySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        只返回当前用户的API秘钥
        """
        return ApiKey.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """
        验证API秘钥有效性
        这里只是一个简单的示例，实际应用中可能需要调用外部API进行验证
        """
        api_key = self.get_object()
        
        # 这里应该添加实际的验证逻辑
        # 例如：调用外部API测试秘钥是否有效
        
        # 模拟验证结果
        is_valid = True
        
        return Response({
            'is_valid': is_valid,
            'message': '秘钥验证成功' if is_valid else '秘钥验证失败'
        })