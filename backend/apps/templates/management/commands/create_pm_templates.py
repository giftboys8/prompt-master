from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建产品运营经理的提示词模板'

    def add_arguments(self, parser):
        parser.add_argument('--user_id', type=int, help='创建模板的用户ID')

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        if not user_id:
            self.stderr.write(self.style.ERROR('请提供用户ID'))
            return

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'用户ID {user_id} 不存在'))
            return

        # 获取框架，如果不存在则创建一个
        framework, created = Framework.objects.get_or_create(
            name='PRODUCT_MANAGER',
            defaults={
                'description': '适合产品运营经理使用的提示词框架'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'创建了新的框架: {framework.name}'))

        templates = [
            {
                "name": "用户需求分析",
                "description": "分析用户需求并提出产品改进建议",
                "content": {
                    "prompt": "作为一名产品运营经理，请根据以下用户反馈进行需求分析，并提出产品改进建议：\n\n用户反馈：{user_feedback}\n\n1. 总结主要用户痛点\n2. 分析这些痛点对用户体验的影响\n3. 提出至少3个具体的产品改进建议\n4. 为每个建议评估可行性和潜在影响\n5. 制定优先级实施计划"
                },
                "variables": ["user_feedback"],
                "target_role": "产品运营经理"
            },
            {
                "name": "竞品分析报告",
                "description": "对竞争对手产品进行全面分析并生成报告",
                "content": {
                    "prompt": "作为产品运营经理，请对我们的主要竞争对手 {competitor_name} 进行全面分析，并生成一份竞品分析报告。报告应包含以下内容：\n\n1. 竞品基本信息（公司背景、市场定位、目标用户）\n2. 产品功能对比（列出我们产品和竞品的主要功能，并进行对比分析）\n3. 用户体验评估（界面设计、易用性、性能等方面）\n4. 营销策略分析（定价、推广渠道、用户获取方式等）\n5. 优势与劣势总结（SWOT分析）\n6. 对我们产品的改进建议和差异化策略"
                },
                "variables": ["competitor_name"],
                "target_role": "产品运营经理"
            },
            {
                "name": "产品上线检查清单",
                "description": "确保产品顺利上线的全面检查清单",
                "content": {
                    "prompt": "作为产品运营经理，你需要确保新产品 {product_name} 顺利上线。请生成一份详细的产品上线检查清单，包括但不限于以下方面：\n\n1. 产品功能测试\n2. 用户界面和体验检查\n3. 性能和稳定性测试\n4. 安全性检查\n5. 数据隐私合规性\n6. 市场营销材料准备\n7. 客户支持团队培训\n8. 监控和分析工具部署\n9. 应急预案制定\n10. 上线后快速反馈机制\n\n对于每个检查项，请提供具体的检查内容和负责人角色建议。"
                },
                "variables": ["product_name"],
                "target_role": "产品运营经理"
            },
            {
                "name": "用户增长策略制定",
                "description": "制定有效的用户增长策略",
                "content": {
                    "prompt": "作为产品运营经理，你需要为产品 {product_name} 制定一个全面的用户增长策略。请考虑以下因素并提出详细的策略建议：\n\n1. 目标用户群体分析\n2. 用户获取渠道评估和选择\n3. 病毒式传播机制设计\n4. 用户激活和留存策略\n5. 用户行为分析和个性化推荐\n6. 社交媒体营销策略\n7. 内容营销计划\n8. 用户反馈收集和产品迭代机制\n9. KPI 设定和监控方案\n10. 预算分配建议\n\n请为每个策略点提供具体的执行建议和预期效果。"
                },
                "variables": ["product_name"],
                "target_role": "产品运营经理"
            },
            {
                "name": "产品运营数据分析报告",
                "description": "分析产品运营数据并提供洞察",
                "content": {
                    "prompt": "作为产品运营经理，请基于以下产品运营数据，生成一份详细的分析报告：\n\n用户增长率：{user_growth_rate}\n日活跃用户数（DAU）：{daily_active_users}\n月活跃用户数（MAU）：{monthly_active_users}\n用户留存率：{retention_rate}\n平均收入per用户（ARPU）：{arpu}\n\n请在报告中包含以下内容：\n\n1. 数据概览和关键指标解读\n2. 用户增长趋势分析\n3. 用户活跃度和粘性评估\n4. 用户留存情况分析\n5. 收入表现评估\n6. 相关指标间的相关性分析\n7. 存在的问题和潜在风险\n8. 改进建议和优化策略\n9. 未来目标和预测\n\n请提供数据可视化建议，并对每个分析点给出actionable的建议。"
                },
                "variables": ["user_growth_rate", "daily_active_users", "monthly_active_users", "retention_rate", "arpu"],
                "target_role": "产品运营经理"
            }
        ]

        created_count = 0
        for template_data in templates:
            # 检查模板是否已存在
            existing = Template.objects.filter(
                name=template_data["name"],
                target_role=template_data["target_role"]
            ).exists()
            
            if not existing:
                Template.objects.create(
                    name=template_data["name"],
                    framework=framework,
                    framework_type=framework.name,
                    description=template_data["description"],
                    content=template_data["content"],
                    variables=template_data["variables"],
                    target_role=template_data["target_role"],
                    created_by=user,
                    visibility='PUBLIC'  # 设置为公开可见
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建模板: {template_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'模板已存在，跳过: {template_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'成功创建 {created_count} 个产品运营经理模板'))