import json
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http import HttpResponse
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .models import Template, TemplateVersion, TemplateTest
from .serializers import TemplateSerializer, TemplateVersionSerializer, TemplateTestSerializer

from django.db.models import Q
import json

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['framework_type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'order']
    parser_classes = [JSONParser, MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.user)
        
        # 添加角色筛选
        target_role = self.request.query_params.get('target_role', None)
        if target_role:
            queryset = queryset.filter(target_role__icontains=target_role)
        
        # 添加模糊搜索（名称、描述和内容）
        search = self.request.query_params.get('search', None)
        if search:
            content_filters = Q()
            
            # 先尝试搜索名称和描述
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
            
            # 然后搜索JSON内容字段
            templates_with_content_match = []
            for template in Template.objects.filter(created_by=self.request.user):
                content = template.content
                if content:
                    # 检查各种可能的内容字段
                    if isinstance(content, str):
                        try:
                            content_dict = json.loads(content)
                        except:
                            content_dict = {}
                    else:
                        content_dict = content
                        
                    for key, value in content_dict.items():
                        if value and isinstance(value, str) and search.lower() in value.lower():
                            templates_with_content_match.append(template.id)
                            break
            
            # 合并内容搜索结果
            if templates_with_content_match:
                queryset = queryset.filter(
                    Q() | Q(id__in=templates_with_content_match)
                )
                
        return queryset
        
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """更新模板排序"""
        try:
            with transaction.atomic():
                order_data = request.data
                for item in order_data:
                    template_id = item.get('id')
                    new_order = item.get('order')
                    
                    if template_id and new_order is not None:
                        template = Template.objects.get(id=template_id, created_by=request.user)
                        template.order = new_order
                        template.save(update_fields=['order'])
                        
                return Response({'message': '排序更新成功'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

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

    @action(detail=False, methods=['get'])
    def export(self, request):
        """导出所有模板"""
        templates = self.get_queryset()
        serializer = self.get_serializer(templates, many=True)
        response = HttpResponse(json.dumps(serializer.data), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="templates_export.json"'
        return response

    @action(detail=False, methods=['post'])
    def import_templates(self, request):
        """导入模板"""
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)

            templates_data = json.loads(file.read())
            imported_count = 0
            for template_data in templates_data:
                template_data['created_by'] = request.user.id
                serializer = self.get_serializer(data=template_data)
                if serializer.is_valid():
                    serializer.save()
                    imported_count += 1

            return Response({'message': f'成功导入 {imported_count} 个模板'})
        except json.JSONDecodeError:
            return Response({'error': '无效的 JSON 文件'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

class TemplateTestViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateTestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['template', 'model']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return TemplateTest.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def run_test(self, request):
        template_id = request.data.get('template')
        model = request.data.get('model')
        input_data = request.data.get('input_data')

        if not all([template_id, model, input_data]):
            return Response({'error': '缺少必要的参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            template = Template.objects.get(id=template_id, created_by=request.user)
        except Template.DoesNotExist:
            return Response({'error': '模板不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 这里应该实现与不同大模型的集成逻辑
        # 目前我们只是模拟一个简单的输出
        output_content = f"这是使用 {model} 模型测试 '{template.name}' 模板的结果。\n\n"
        output_content += "输入数据：\n```json\n" + json.dumps(input_data, indent=2, ensure_ascii=False) + "\n```\n\n"
        output_content += "模拟输出：\n这是一个模拟的输出结果，实际实现时需要集成相应的大模型API。"

        test = TemplateTest.objects.create(
            template=template,
            model=model,
            input_data=input_data,
            output_content=output_content,
            created_by=request.user
        )

        serializer = self.get_serializer(test)
        return Response(serializer.data)