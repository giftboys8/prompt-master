from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Scene, SceneTask, SceneVersion, SceneUsage
from .serializers import (
    SceneListSerializer,
    SceneDetailSerializer,
    SceneCreateUpdateSerializer,
    SceneTaskSerializer,
    SceneVersionSerializer,
    SceneUsageSerializer,
    ScenePreviewSerializer
)


class SceneViewSet(viewsets.ModelViewSet):
    """场景管理视图集"""
    queryset = Scene.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'list':
            return SceneListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SceneCreateUpdateSerializer
        return SceneDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        # 按角色筛选
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(target_roles__contains=[role])
        
        return queryset

    @action(detail=True, methods=['post'])
    def create_version(self, request, pk=None):
        """创建新版本"""
        scene = self.get_object()
        
        # 获取版本描述
        description = request.data.get('description', '')
        
        # 构建版本内容
        content = {
            'scene': {
                'name': scene.name,
                'category': scene.category,
                'description': scene.description,
                'target_roles': scene.target_roles,
                'status': scene.status,
            },
            'tasks': list(scene.tasks.values()),
        }
        
        # 创建新版本
        version = SceneVersion.objects.create(
            scene=scene,
            version_number=scene.version,
            description=description,
            content=content,
            created_by=request.user
        )
        
        serializer = SceneVersionSerializer(version)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """获取版本历史"""
        scene = self.get_object()
        versions = scene.versions.all().order_by('-created_at')
        
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = SceneVersionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = SceneVersionSerializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='versions/(?P<version_id>[^/.]+)/rollback')
    def rollback_version(self, request, pk=None, version_id=None):
        """版本回滚"""
        scene = self.get_object()
        
        try:
            version = SceneVersion.objects.get(id=version_id, scene=scene)
        except SceneVersion.DoesNotExist:
            return Response(
                {"error": "Version not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 获取版本内容
        content = version.content
        scene_data = content.get('scene', {})
        tasks_data = content.get('tasks', [])
        templates_data = content.get('templates', [])
        
        # 更新场景基本信息
        for key, value in scene_data.items():
            if hasattr(scene, key):
                setattr(scene, key, value)
        
        # 生成新版本号
        current_version = scene.version.split('.')
        if len(current_version) >= 2:
            major, minor = current_version[0], current_version[1]
            scene.version = f"{major}.{int(minor) + 1}"
        else:
            scene.version = f"{scene.version}.1"
        
        scene.save()
        
        # 删除现有任务并创建新任务
        scene.tasks.all().delete()
        for task_data in tasks_data:
            # 移除ID和创建时间等字段
            if 'id' in task_data:
                del task_data['id']
            if 'created_at' in task_data:
                del task_data['created_at']
            
            SceneTask.objects.create(scene=scene, **task_data)
        
        # 不再需要处理模板关联，因为现在模板直接与任务关联
        
        # 创建回滚版本记录
        rollback_version = SceneVersion.objects.create(
            scene=scene,
            version_number=scene.version,
            description=f"回滚至版本 {version.version_number}",
            content={
                'scene': {
                    'name': scene.name,
                    'category': scene.category,
                    'description': scene.description,
                    'target_roles': scene.target_roles,
                    'status': scene.status,
                },
                'tasks': list(scene.tasks.values()),
            },
            created_by=request.user
        )
        
        serializer = SceneDetailSerializer(scene)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """获取场景预览信息"""
        scene = self.get_object()
        serializer = ScenePreviewSerializer(scene)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """获取相似场景"""
        scene = self.get_object()
        
        # 简单实现：基于相同分类和目标角色查找
        similar_scenes = Scene.objects.filter(
            Q(category=scene.category) | 
            Q(target_roles__overlap=scene.target_roles)
        ).exclude(id=scene.id)[:5]
        
        serializer = SceneListSerializer(similar_scenes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """提交使用反馈"""
        scene = self.get_object()
        template_id = request.data.get('template_id')
        feedback_score = request.data.get('feedback_score')
        feedback_content = request.data.get('feedback_content', '')
        
        # 创建或更新使用记录
        usage, created = SceneUsage.objects.get_or_create(
            scene=scene,
            user=request.user,
            template_id=template_id,
            defaults={
                'feedback_score': feedback_score,
                'feedback_content': feedback_content
            }
        )
        
        if not created:
            usage.feedback_score = feedback_score
            usage.feedback_content = feedback_content
            usage.save()
        
        serializer = SceneUsageSerializer(usage)
        return Response(serializer.data)


class SceneTaskViewSet(viewsets.ModelViewSet):
    """场景任务视图集"""
    queryset = SceneTask.objects.all()
    serializer_class = SceneTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scene', 'template']


class RecommendationViewSet(viewsets.ViewSet):
    """推荐系统视图集"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def scenes(self, request):
        """获取推荐场景"""
        user = request.user
        role = request.query_params.get('role', '')
        
        # 简单实现：基于用户历史使用记录和角色推荐
        # 1. 获取用户使用过的场景
        used_scenes = SceneUsage.objects.filter(
            user=user
        ).values_list('scene_id', flat=True)
        
        # 2. 基于角色筛选场景
        if role:
            recommended_scenes = Scene.objects.filter(
                target_roles__contains=[role]
            ).exclude(
                id__in=used_scenes
            )[:5]
        else:
            # 如果没有指定角色，推荐使用频率高的场景
            popular_scenes = SceneUsage.objects.values('scene').annotate(
                count=models.Count('scene')
            ).order_by('-count')[:5]
            
            recommended_scenes = Scene.objects.filter(
                id__in=[item['scene'] for item in popular_scenes]
            ).exclude(
                id__in=used_scenes
            )
        
        serializer = SceneListSerializer(recommended_scenes, many=True)
        return Response(serializer.data)