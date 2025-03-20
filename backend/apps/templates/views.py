from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Template, TemplateVersion
from .serializers import TemplateSerializer, TemplateVersionSerializer

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['framework_type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """克隆模板"""
        template = self.get_object()
        new_template = Template.objects.create(
            name=f"{template.name} (副本)",
            framework_type=template.framework_type,
            description=template.description,
            content=template.content,
            variables=template.variables,
            created_by=request.user
        )
        serializer = self.get_serializer(new_template)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """获取模板的所有版本"""
        template = self.get_object()
        versions = template.versions.all()
        serializer = TemplateVersionSerializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """恢复到指定版本"""
        template = self.get_object()
        version_id = request.data.get('version_id')
        
        try:
            version = template.versions.get(id=version_id)
            version.restore()
            return Response({'message': '恢复成功'})
        except TemplateVersion.DoesNotExist:
            return Response(
                {'error': '指定版本不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TemplateVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """模板版本只读视图集"""
    serializer_class = TemplateVersionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['template', 'version_number']
    ordering_fields = ['version_number', 'created_at']

    def get_queryset(self):
        return TemplateVersion.objects.filter(
            template__created_by=self.request.user
        )