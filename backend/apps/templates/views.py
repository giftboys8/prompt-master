import json
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http import HttpResponse
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Template, TemplateVersion, TemplateTest, SharedTemplate
from .serializers import TemplateSerializer, TemplateVersionSerializer, TemplateTestSerializer
from .filters import TemplateFilter

from django.db.models import Q

User = get_user_model()

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TemplateFilter  # 使用自定义的过滤器类
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'order']
    parser_classes = [JSONParser, MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        try:
            # 获取用户创建的模板和分享给用户的模板
            queryset = Template.objects.filter(
                Q(created_by=self.request.user) |
                Q(shares__shared_with=self.request.user) |
                Q(visibility='PUBLIC')
            ).distinct()
            
            # 添加角色筛选
            # 注意：主要的角色筛选逻辑已经在 TemplateFilter 中处理
            # 这里仅作为备用，当 filterset_class 未生效时使用
            target_role = self.request.query_params.get('target_role', None)
            if target_role and not hasattr(self, 'filterset_class'):
                # 尝试解析JSON数组
                try:
                    roles = json.loads(target_role)
                    if isinstance(roles, list):
                        # 如果是列表，我们需要检查任何一个角色是否匹配
                        queryset = queryset.filter(target_role__overlap=roles)
                    else:
                        # 如果不是列表，就当作单个值处理
                        queryset = queryset.filter(target_role__contains=[roles])
                except json.JSONDecodeError:
                    # 如果不是有效的JSON，就当作单个字符串处理
                    value = target_role.strip('[]').replace('\"', '').strip()
                    # 使用 PostgreSQL 的 jsonb_path_exists 函数来实现不区分大小写的搜索
                    queryset = queryset.filter(target_role__contains=[value]) | \
                               queryset.extra(
                                   where=["jsonb_path_exists(target_role, '$ ? (@[*] like_regex \"(?i)^.*' || %s || '.*$\")')"],
                                   params=[value]
                               )
            
            # 添加模糊搜索（名称和描述）
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )
            
            return queryset
            
        except Exception as e:
            # 记录错误但返回空查询集
            print(f"Error in get_queryset: {str(e)}")
            return Template.objects.none()
        
        # 合并内容搜索结果
        if 'templates_with_content_match' in locals() and templates_with_content_match:
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
        import traceback
        import sys
        
        try:
            # 获取原模板
            template = self.get_object()
            print(f"开始克隆模板 ID: {pk}, 名称: {template.name}")
            
            try:
                # 使用事务确保原子性
                with transaction.atomic():
                    # 创建新模板实例
                    new_template = Template.objects.create(
                        name=f"{template.name} (副本)",
                        framework=template.framework,
                        framework_type=template.framework_type,  # 保持原模板的框架类型
                        description=template.description,
                        content=template.content,
                        variables=template.variables,
                        target_role=template.target_role,
                        order=template.order,
                        created_by=request.user,
                        visibility='PRIVATE'  # 克隆的模板默认设置为私有
                    )
                    print(f"成功创建新模板 ID: {new_template.id}")
                    
                    # 序列化并返回新模板数据
                    serializer = self.get_serializer(new_template)
                    return Response(serializer.data)
            except Exception as e:
                print(f"模板创建失败: {str(e)}")
                traceback.print_exc(file=sys.stdout)
                return Response({"error": f"创建模板失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            print(f"克隆操作失败: {str(e)}")
            traceback.print_exc(file=sys.stdout)
            return Response({"error": f"克隆失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Template.DoesNotExist:
            return Response(
                {'error': '要克隆的模板不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'克隆模板失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """分享模板给其他用户"""
        template = self.get_object()
        
        # 只有创建者可以分享模板
        if template.created_by != request.user:
            return Response(
                {'error': '只有模板创建者可以分享模板'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 获取要分享给的用户和权限设置
        user_id = request.data.get('user_id')
        can_edit = request.data.get('can_edit', False)
        
        try:
            shared_with = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': '指定的用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # 不能分享给自己
        if shared_with == request.user:
            return Response(
                {'error': '不能分享给自己'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 创建或更新分享记录
        share, created = SharedTemplate.objects.update_or_create(
            template=template,
            shared_with=shared_with,
            defaults={
                'can_edit': can_edit,
                'created_by': request.user
            }
        )
        
        return Response(
            {'message': f'已成功分享给 {shared_with.username}', 'created': created},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
    @action(detail=True, methods=['delete'])
    def revoke_share(self, request, pk=None):
        """撤销模板分享"""
        template = self.get_object()
        
        # 只有创建者可以撤销分享
        if template.created_by != request.user:
            return Response(
                {'error': '只有模板创建者可以撤销分享'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        
        try:
            shared_with = User.objects.get(id=user_id)
            share = SharedTemplate.objects.get(
                template=template,
                shared_with=shared_with
            )
            share.delete()
            return Response({'message': f'已撤销与 {shared_with.username} 的分享'})
        except User.DoesNotExist:
            return Response(
                {'error': '指定的用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except SharedTemplate.DoesNotExist:
            return Response(
                {'error': '未找到分享记录'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=True, methods=['get'])
    def get_shares(self, request, pk=None):
        """获取模板的共享列表"""
        template = self.get_object()
        
        # 只有创建者可以查看分享列表
        if template.created_by != request.user:
            return Response(
                {'error': '只有模板创建者可以查看分享列表'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 获取该模板的所有分享记录
        shares = SharedTemplate.objects.filter(template=template)
        
        # 构建响应数据
        share_data = []
        for share in shares:
            share_data.append({
                'id': share.id,
                'template': share.template.id,
                'template_name': share.template.name,
                'shared_with': {
                    'id': share.shared_with.id,
                    'username': share.shared_with.username,
                    'email': share.shared_with.email,
                    'is_staff': share.shared_with.is_staff,
                    'date_joined': share.shared_with.date_joined
                },
                'created_by': {
                    'id': share.created_by.id,
                    'username': share.created_by.username,
                    'email': share.created_by.email,
                    'is_staff': share.created_by.is_staff,
                    'date_joined': share.created_by.date_joined
                },
                'can_edit': share.can_edit,
                'status': 'accepted',  # 直接分享的状态默认为accepted
                'created_at': share.created_at
            })
        
        return Response(share_data)
        
    @action(detail=True, methods=['get'])
    def get_share(self, request, pk=None):
        """获取单个模板的分享信息"""
        template = self.get_object()
        
        # 获取用户ID参数
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {'error': '缺少必要的用户ID参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # 查找分享记录
            share = SharedTemplate.objects.get(
                template=template,
                shared_with_id=user_id
            )
            
            # 构建响应数据
            share_data = {
                'id': share.id,
                'template': share.template.id,
                'template_name': share.template.name,
                'shared_with': {
                    'id': share.shared_with.id,
                    'username': share.shared_with.username,
                    'email': share.shared_with.email,
                    'is_staff': share.shared_with.is_staff,
                    'date_joined': share.shared_with.date_joined
                },
                'created_by': {
                    'id': share.created_by.id,
                    'username': share.created_by.username,
                    'email': share.created_by.email,
                    'is_staff': share.created_by.is_staff,
                    'date_joined': share.created_by.date_joined
                },
                'can_edit': share.can_edit,
                'status': share.status,
                'created_at': share.created_at
            }
            
            return Response(share_data)
            
        except SharedTemplate.DoesNotExist:
            return Response(
                {'error': '未找到该模板与指定用户的分享记录'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def shared_with_me(self, request):
        """获取分享给我的模板列表"""
        shared_templates = Template.objects.filter(
            shares__shared_with=request.user
        )
        
        # 添加筛选和排序
        target_role = request.query_params.get('target_role', None)
        if target_role:
            shared_templates = shared_templates.filter(target_role__icontains=target_role)
            
        # 添加搜索
        search = request.query_params.get('search', None)
        if search:
            shared_templates = shared_templates.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
            
        # 排序
        ordering = request.query_params.get('ordering', '-created_at')
        shared_templates = shared_templates.order_by(ordering)
        
        # 分页
        page = self.paginate_queryset(shared_templates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(shared_templates, many=True)
        return Response(serializer.data)
        
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
    queryset = TemplateTest.objects.all()
    serializer_class = TemplateTestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['template']
    search_fields = ['model']
    
    def get_queryset(self):
        return TemplateTest.objects.filter(
            template__created_by=self.request.user
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            # 从请求数据中获取必要字段
            template_id = request.data.get('template')
            model = request.data.get('model')
            input_data = request.data.get('input_data')
            output_content = request.data.get('output_content')
            dify_response = request.data.get('dify_response')

            # 打印请求数据以便调试
            print(f"接收到测试记录保存请求: template_id={template_id}, model={model}")
            print(f"input_data: {input_data}")
            print(f"output_content: {output_content}")

            # 获取模板对象
            try:
                template = Template.objects.get(id=template_id)
            except Template.DoesNotExist:
                return Response(
                    {'error': f'Template with id {template_id} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 创建测试记录
            test = TemplateTest.objects.create(
                template=template,
                model=model,
                input_data=input_data,
                output_content=output_content,
                dify_response=dify_response,
                created_by=request.user
            )

            # 序列化并返回响应
            serializer = self.get_serializer(test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"创建测试记录时发生错误: {str(e)}")
            return Response(
                {'error': f'Failed to create test record: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def run_test(self, request):
        template_id = request.data.get('template')
        model = request.data.get('model')
        input_data = request.data.get('input_data')
        dry_run = request.data.get('dryRun', False)
        dify_response = request.data.get('dify_response')
        output_content = request.data.get('output_content')

        print(f"接收到测试记录保存请求: template_id={template_id}, model={model}")
        print(f"input_data: {input_data}")
        print(f"dify_response 类型: {type(dify_response)}")
        print(f"output_content: {output_content}")

        # 打印完整的请求数据
        print(f"完整的请求数据: {request.data}")

        if not all([template_id, model, input_data]):
            return Response({'error': '缺少必要的参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 首先尝试查找用户创建的模板
            template = Template.objects.filter(
                id=template_id
            ).filter(
                Q(created_by=request.user) | Q(shares__shared_with=request.user)
            ).first()
            
            if not template:
                return Response({'error': '模板不存在或您没有权限访问此模板'}, status=status.HTTP_404_NOT_FOUND)
        except Template.DoesNotExist:
            return Response({'error': '模板不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 生成提示词
        prompt = self._generate_prompt(template, input_data)

        if dry_run:
            # 只返回生成的提示词，不实际执行测试
            return Response({'prompt': prompt})

        # 如果提供了Dify响应，使用它；否则使用模拟输出
        if dify_response:
            output_content = json.dumps({
                'answer': dify_response.get('answer', '未获取到有效响应'),
                'prompt': prompt,
                'model': model,
                'input_variables': input_data,
                'template_name': template.name,
                'framework_type': template.framework_type
            }, ensure_ascii=False, indent=2)
        else:
            # 模拟输出（用于开发测试）
            output_content = json.dumps({
                'answer': f"这是使用 {model} 模型测试 '{template.name}' 模板的结果。\n\n模拟输出：这是一个模拟的输出结果，实际实现时需要集成相应的大模型API。",
                'prompt': prompt,
                'model': model,
                'input_variables': input_data,
                'template_name': template.name,
                'framework_type': template.framework_type
            }, ensure_ascii=False, indent=2)

        try:
            test = TemplateTest.objects.create(
                template=template,
                model=model,
                input_data=input_data,
                output_content=output_content,
                prompt=prompt,
                dify_response=dify_response,
                created_by=request.user
            )

            serializer = self.get_serializer(test)
            return Response(serializer.data)
        except Exception as e:
            print(f"创建测试记录时发生错误: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_prompt(self, template, input_data):
        """根据模板和输入数据生成提示词"""
        if template.framework_type == 'CUSTOM' or not template.framework:
            prompt = template.content.get('custom', '')
        elif template.framework_type == 'RTGO':
            prompt = f"# 角色（Role）\n{template.content['role']}\n\n"
            prompt += f"# 任务（Task）\n{template.content['task']}\n\n"
            prompt += f"# 目标（Goal）\n{template.content['goal']}\n\n"
            prompt += f"# 输出（Output）\n{template.content['output']}\n\n"
        elif template.framework_type == 'SPAR':
            prompt = f"# 情况（Situation）\n{template.content['situation']}\n\n"
            prompt += f"# 目的（Purpose）\n{template.content['purpose']}\n\n"
            prompt += f"# 行动（Action）\n{template.content['action']}\n\n"
            prompt += f"# 结果（Result）\n{template.content['result']}\n\n"
        else:
            prompt = template.content.get('custom', '')

        # 替换变量
        for var in template.variables:
            var_name = var['name']
            if var_name in input_data:
                prompt = prompt.replace(f"{{${var_name}}}", str(input_data[var_name]))

        return prompt