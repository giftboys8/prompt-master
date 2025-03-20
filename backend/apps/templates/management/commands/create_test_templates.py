from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试用的提示词模板数据'

    def handle(self, *args, **kwargs):
        # 确保有一个超级用户
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write('创建超级用户...')
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )

        # 创建测试模板
        templates_data = [
            {
                'name': '文章写作助手',
                'framework_type': 'RTGO',
                'description': '帮助用户生成高质量的文章内容',
                'content': {
                    'role': '专业文章写作助手',
                    'task': '根据用户提供的主题和关键词，生成一篇结构完整的文章',
                    'goal': '生成一篇逻辑清晰、内容丰富、语言流畅的文章',
                    'output': '输出一篇包含标题、引言、正文和总结的文章'
                },
                'variables': [
                    {
                        'name': 'topic',
                        'default_value': '人工智能的未来发展',
                        'description': '文章主题'
                    },
                    {
                        'name': 'keywords',
                        'default_value': '机器学习,深度学习,神经网络',
                        'description': '关键词列表'
                    },
                    {
                        'name': 'word_count',
                        'default_value': '1000',
                        'description': '目标字数'
                    }
                ]
            },
            {
                'name': '营销文案生成器',
                'framework_type': 'SPAR',
                'description': '帮助用户生成吸引人的营销文案',
                'content': {
                    'situation': '在社交媒体平台上推广产品或服务',
                    'purpose': '吸引目标用户的注意力并提高转化率',
                    'action': '生成简短、吸引人且具有说服力的营销文案',
                    'result': '提供多个版本的文案供用户选择'
                },
                'variables': [
                    {
                        'name': 'product_name',
                        'default_value': '智能手表',
                        'description': '产品名称'
                    },
                    {
                        'name': 'target_audience',
                        'default_value': '25-35岁的年轻白领',
                        'description': '目标受众'
                    },
                    {
                        'name': 'key_features',
                        'default_value': '心率监测,睡眠分析,运动追踪',
                        'description': '产品主要特点'
                    }
                ]
            },
            {
                'name': '自定义提示词模板',
                'framework_type': 'CUSTOM',
                'description': '完全自定义的提示词模板',
                'content': {
                    'custom': """作为一个{role}，你需要帮助用户完成以下任务：

1. 背景信息：
{background}

2. 具体要求：
{requirements}

3. 输出格式：
{output_format}

请确保输出内容符合以上要求。"""
                },
                'variables': [
                    {
                        'name': 'role',
                        'default_value': '专业顾问',
                        'description': '角色定位'
                    },
                    {
                        'name': 'background',
                        'default_value': '项目背景描述',
                        'description': '背景信息'
                    },
                    {
                        'name': 'requirements',
                        'default_value': '具体任务要求',
                        'description': '具体要求'
                    },
                    {
                        'name': 'output_format',
                        'default_value': '输出格式说明',
                        'description': '输出格式'
                    }
                ]
            }
        ]

        # 创建模板
        for template_data in templates_data:
            Template.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    **template_data,
                    'created_by': admin_user
                }
            )

        self.stdout.write(self.style.SUCCESS('成功创建测试模板数据！'))