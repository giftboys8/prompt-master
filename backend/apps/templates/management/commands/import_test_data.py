import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template, TemplateVersion, SharedTemplate, TemplateTest

User = get_user_model()

class Command(BaseCommand):
    help = '导入测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始导入测试数据...')
        
        # 创建测试用户
        self.create_test_users()
        
        # 创建模板和相关数据
        self.create_templates()
        
        self.stdout.write(self.style.SUCCESS('测试数据导入完成!'))
    
    def create_test_users(self):
        self.stdout.write('创建测试用户...')
        
        # 创建管理员用户
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'创建管理员用户: {admin_user.username}')
        else:
            self.stdout.write(f'管理员用户已存在: {admin_user.username}')
        
        # 创建普通用户
        test_users = [
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'user123'},
            {'username': 'user2', 'email': 'user2@example.com', 'password': 'user123'},
            {'username': 'user3', 'email': 'user3@example.com', 'password': 'user123'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'创建普通用户: {user.username}')
            else:
                self.stdout.write(f'普通用户已存在: {user.username}')
    
    def create_templates(self):
        self.stdout.write('创建模板数据...')
        
        # 获取用户
        admin = User.objects.get(username='admin')
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        
        # 创建RTGO框架模板
        rtgo_template_data = {
            'name': 'RTGO测试模板',
            'visibility': 'PUBLIC',
            'framework_type': 'RTGO',
            'description': 'RTGO框架的测试模板',
            'content': {
                'role': '你是一个专业的技术文档编写者',
                'task': '编写清晰、简洁的API文档',
                'goal': '帮助开发者快速理解和使用API',
                'output': '包含标题、描述、参数说明和示例的Markdown格式文档'
            },
            'variables': [
                {'name': 'api_name', 'description': 'API名称', 'required': True},
                {'name': 'api_version', 'description': 'API版本', 'required': False},
            ],
            'order': 1,
            'target_role': '技术文档编写',
            'created_by': admin
        }
        
        rtgo_template = Template.objects.create(**rtgo_template_data)
        self.stdout.write(f'创建RTGO模板: {rtgo_template.name}')
        
        # 创建SPAR框架模板
        spar_template_data = {
            'name': 'SPAR测试模板',
            'visibility': 'PRIVATE',
            'framework_type': 'SPAR',
            'description': 'SPAR框架的测试模板',
            'content': {
                'situation': '你正在为一个电子商务网站编写产品描述',
                'problem': '需要吸引顾客并提供准确的产品信息',
                'action': '分析产品特点，编写吸引人的描述',
                'result': '生成一个包含关键特性、优势和使用场景的产品描述'
            },
            'variables': [
                {'name': 'product_name', 'description': '产品名称', 'required': True},
                {'name': 'product_category', 'description': '产品类别', 'required': True},
                {'name': 'target_audience', 'description': '目标受众', 'required': False},
            ],
            'order': 2,
            'target_role': '营销内容创作',
            'created_by': user1
        }
        
        spar_template = Template.objects.create(**spar_template_data)
        self.stdout.write(f'创建SPAR模板: {spar_template.name}')
        
        # 创建自定义框架模板
        custom_template_data = {
            'name': '自定义测试模板',
            'visibility': 'SHARED',
            'framework_type': 'CUSTOM',
            'description': '自定义框架的测试模板',
            'content': {
                'system': '你是一个创意写作助手',
                'user': '我需要一个关于{{topic}}的短故事，风格是{{style}}',
                'assistant': '好的，我会为您创作一个关于{{topic}}的{{style}}风格短故事'
            },
            'variables': [
                {'name': 'topic', 'description': '故事主题', 'required': True},
                {'name': 'style', 'description': '写作风格', 'required': True},
                {'name': 'length', 'description': '故事长度(字数)', 'required': False},
            ],
            'order': 3,
            'target_role': '创意写作',
            'created_by': user2
        }
        
        custom_template = Template.objects.create(**custom_template_data)
        self.stdout.write(f'创建自定义模板: {custom_template.name}')
        
        # 创建模板分享记录
        shared_template_data = {
            'template': custom_template,
            'shared_with': user1,
            'can_edit': True,
            'status': 'ACCEPTED',
            'created_by': user2
        }
        
        SharedTemplate.objects.create(**shared_template_data)
        self.stdout.write(f'创建模板分享记录: {custom_template.name} -> {user1.username}')
        
        # 创建模板测试记录
        template_test_data = {
            'template': rtgo_template,
            'model': 'GPT-4',
            'input_data': {
                'api_name': 'User Authentication API',
                'api_version': 'v1.0'
            },
            'output_content': '# User Authentication API v1.0\n\n这个API提供了用户认证相关的功能，包括登录、注册、密码重置等操作。\n\n## 端点\n\n- POST /api/auth/login\n- POST /api/auth/register\n- POST /api/auth/reset-password\n\n## 示例\n\n```json\n{\n  "username": "testuser",\n  "password": "password123"\n}\n```',
            'prompt': '你是一个专业的技术文档编写者。你的任务是编写清晰、简洁的API文档，目标是帮助开发者快速理解和使用API。请为名为"User Authentication API"，版本为"v1.0"的API编写一份包含标题、描述、参数说明和示例的Markdown格式文档。',
            'dify_response': {
                'success': True,
                'request_id': 'test-request-id-123',
                'elapsed_time': 2.5
            },
            'created_by': admin
        }
        
        TemplateTest.objects.create(**template_test_data)
        self.stdout.write(f'创建模板测试记录: {rtgo_template.name}')