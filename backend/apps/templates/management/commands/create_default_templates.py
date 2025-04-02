from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from templates.models import Template
from frameworks.models import Framework

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default templates'

    def handle(self, *args, **kwargs):
        # 确保有一个超级用户
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR('No superuser found. Please create a superuser first.'))
            return

        # 获取或创建默认框架
        default_framework, _ = Framework.objects.get_or_create(
            name="Default",
            defaults={
                "description": "Default framework for templates",
                "created_by": superuser
            }
        )

        # 定义默认模板
        default_templates = [
            {
                "name": "业务场景分析",
                "framework_type": "CUSTOM",
                "framework": default_framework,
                "visibility": "PUBLIC",
                "description": "分析特定业务场景，提供深入洞察",
                "content": {
                    "prompt": "请分析以下业务场景：\n\n{scenario}\n\n1. 主要挑战：\n2. 潜在机会：\n3. 关键利益相关者：\n4. 可能的解决方案：\n5. 实施建议：",
                    "variables": [
                        {"name": "scenario", "description": "需要分析的具体业务场景描述"}
                    ]
                },
                "variables": [
                    {"name": "scenario", "description": "需要分析的具体业务场景描述"}
                ],
                "target_role": "产品经理"
            },
            {
                "name": "用户需求收集",
                "framework_type": "CUSTOM",
                "framework": default_framework,
                "visibility": "PUBLIC",
                "description": "收集和整理用户需求的模板",
                "content": {
                    "prompt": "请帮助收集以下产品的用户需求：\n\n产品：{product}\n\n1. 目标用户群体：\n2. 主要痛点：\n3. 期望的核心功能：\n4. 使用场景：\n5. 可能的顾虑：\n6. 竞品比较：\n7. 改进建议：",
                    "variables": [
                        {"name": "product", "description": "需要收集用户需求的产品名称"}
                    ]
                },
                "variables": [
                    {"name": "product", "description": "需要收集用户需求的产品名称"}
                ],
                "target_role": "产品经理"
            },
            {
                "name": "产品功能规划",
                "framework_type": "CUSTOM",
                "framework": default_framework,
                "visibility": "PUBLIC",
                "description": "规划产品功能和路线图",
                "content": {
                    "prompt": "请为以下产品制定功能规划和路线图：\n\n产品：{product}\n当前阶段：{stage}\n\n1. 核心功能列表：\n2. 优先级排序：\n3. 开发周期估算：\n4. 潜在技术挑战：\n5. 用户价值点：\n6. 后续迭代方向：\n7. 成功指标：",
                    "variables": [
                        {"name": "product", "description": "需要规划的产品名称"},
                        {"name": "stage", "description": "产品当前所处的开发阶段"}
                    ]
                },
                "variables": [
                    {"name": "product", "description": "需要规划的产品名称"},
                    {"name": "stage", "description": "产品当前所处的开发阶段"}
                ],
                "target_role": "产品经理"
            },
            {
                "name": "竞品分析报告",
                "framework_type": "CUSTOM",
                "framework": default_framework,
                "visibility": "PUBLIC",
                "description": "全面分析竞争对手的产品",
                "content": {
                    "prompt": "请对以下竞品进行详细分析：\n\n我们的产品：{our_product}\n竞品：{competitor_product}\n\n1. 产品定位对比：\n2. 核心功能对比：\n3. 用户体验对比：\n4. 定价策略对比：\n5. 市场份额分析：\n6. 优势与劣势：\n7. 潜在威胁：\n8. 我们的应对策略：",
                    "variables": [
                        {"name": "our_product", "description": "我们的产品名称"},
                        {"name": "competitor_product", "description": "竞争对手的产品名称"}
                    ]
                },
                "variables": [
                    {"name": "our_product", "description": "我们的产品名称"},
                    {"name": "competitor_product", "description": "竞争对手的产品名称"}
                ],
                "target_role": "产品经理"
            },
            {
                "name": "用户反馈分析",
                "framework_type": "CUSTOM",
                "framework": default_framework,
                "visibility": "PUBLIC",
                "description": "分析用户反馈并提出改进建议",
                "content": {
                    "prompt": "请分析以下用户反馈并提供改进建议：\n\n产品：{product}\n用户反馈：{feedback}\n\n1. 关键问题总结：\n2. 用户痛点分析：\n3. 积极反馈点：\n4. 改进优先级：\n5. 具体改进建议：\n6. 长期改进方向：\n7. 用户沟通策略：",
                    "variables": [
                        {"name": "product", "description": "接受反馈的产品名称"},
                        {"name": "feedback", "description": "用户提供的具体反馈内容"}
                    ]
                },
                "variables": [
                    {"name": "product", "description": "接受反馈的产品名称"},
                    {"name": "feedback", "description": "用户提供的具体反馈内容"}
                ],
                "target_role": "产品经理"
            }
        ]

        # 创建模板
        for template_data in default_templates:
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    "framework_type": template_data['framework_type'],
                    "framework": template_data['framework'],
                    "visibility": template_data['visibility'],
                    "description": template_data['description'],
                    "content": template_data['content'],
                    "variables": template_data['variables'],
                    "target_role": template_data['target_role'],
                    "created_by": superuser
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created template "{template.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Template "{template.name}" already exists'))

        self.stdout.write(self.style.SUCCESS('Default templates creation completed'))