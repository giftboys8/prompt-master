from django.core.management.base import BaseCommand
from apps.scenes.models import Scene, SceneTask
from apps.templates.models import Template
from frameworks.models import Framework
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a business analysis scene for product managers'

    def handle(self, *args, **kwargs):
        # 获取管理员用户
        admin_user = User.objects.get(username='admin')
        
        # 获取框架
        costar_framework = Framework.objects.get(name='COSTAR框架')
        crispr_framework = Framework.objects.get(name='CRISPR框架')
        
        # 创建场景
        scene = Scene.objects.create(
            name="业务研发管理产品竞品分析",
            category="产品分析",
            description="全面分析业务研发管理产品的竞品情况，包括功能对比、用户体验、价格策略等多个维度",
            target_roles=["产品经理"],
            status=True,
            created_by=admin_user,
            version="v1.0.0"
        )

        # 定义模板
        templates = [
            {
                "name": "竞品分析框架",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架进行竞品选择和市场定位分析",
                "content": {
                    "Context": "分析市场现状、竞争格局和目标用户需求",
                    "Objective": "确定竞品分析目标和关注重点",
                    "Scope": "界定竞品范围和分析维度",
                    "Task": "制定竞品调研和分析计划",
                    "Action": "执行竞品分析和数据收集",
                    "Result": "输出竞品分析报告和市场定位建议"
                },
                "variables": [
                    {
                        "name": "product_category",
                        "description": "产品类别",
                        "default": "业务研发管理产品"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 1
            },
            {
                "name": "功能对比矩阵生成",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架生成竞品功能对比矩阵",
                "content": {
                    "Context": "了解各竞品的功能特性和技术实现",
                    "Request": "确定功能对比的评估标准和权重",
                    "Intent": "明确功能对比的目的和重点关注领域",
                    "Specifics": "详细列举功能对比项并进行评分",
                    "Persona": "从不同用户角度评估功能实用性",
                    "Response": "生成功能对比矩阵和改进建议"
                },
                "variables": [
                    {
                        "name": "competitor_list",
                        "description": "竞品清单",
                        "default": "主要竞品名称列表"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 2
            },
            {
                "name": "用户体验评估",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架评估竞品用户体验",
                "content": {
                    "Context": "了解用户使用场景和体验需求",
                    "Objective": "设定用户体验评估目标",
                    "Scope": "确定评估范围和关键指标",
                    "Task": "制定用户体验测试方案",
                    "Action": "执行体验评估和数据收集",
                    "Result": "输出体验评估报告和改进建议"
                },
                "variables": [
                    {
                        "name": "ux_dimensions",
                        "description": "体验维度",
                        "default": "易用性/性能/界面/交互"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 3
            },
            {
                "name": "定价策略分析",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架分析竞品定价策略",
                "content": {
                    "Context": "分析市场价格水平和用户支付意愿",
                    "Request": "明确定价策略分析目标",
                    "Intent": "理解竞品定价逻辑和商业模式",
                    "Specifics": "详细对比价格构成和收费方式",
                    "Persona": "评估不同客户群的价格承受能力",
                    "Response": "提出定价策略建议"
                },
                "variables": [
                    {
                        "name": "price_factors",
                        "description": "价格因素",
                        "default": "基础价/附加服务/折扣策略"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 4
            },
            {
                "name": "技术架构评估",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架评估竞品技术架构",
                "content": {
                    "Context": "了解技术发展趋势和行业标准",
                    "Objective": "确定技术评估目标",
                    "Scope": "界定技术评估范围",
                    "Task": "制定技术分析方案",
                    "Action": "执行技术评估",
                    "Result": "输出技术评估报告"
                },
                "variables": [
                    {
                        "name": "tech_aspects",
                        "description": "技术方面",
                        "default": "架构/性能/安全/扩展性"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 5
            },
            {
                "name": "客户服务评估",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架评估竞品客户服务",
                "content": {
                    "Context": "了解客户服务现状和需求",
                    "Request": "明确服务评估目标",
                    "Intent": "分析服务策略和方法",
                    "Specifics": "详细评估服务质量和效率",
                    "Persona": "从客户角度评价服务体验",
                    "Response": "提出服务改进建议"
                },
                "variables": [
                    {
                        "name": "service_metrics",
                        "description": "服务指标",
                        "default": "响应时间/解决率/满意度"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 6
            },
            {
                "name": "SWOT分析",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架进行SWOT分析",
                "content": {
                    "Context": "了解竞品在市场中的表现",
                    "Objective": "确定SWOT分析目标",
                    "Scope": "界定分析范围",
                    "Task": "识别优势、劣势、机会和威胁",
                    "Action": "深入分析各要素",
                    "Result": "输出SWOT分析报告"
                },
                "variables": [
                    {
                        "name": "analysis_focus",
                        "description": "分析重点",
                        "default": "市场/产品/技术/团队"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 7
            },
            {
                "name": "竞争策略制定",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架制定竞争策略",
                "content": {
                    "Context": "综合分析竞争环境",
                    "Request": "明确战略目标",
                    "Intent": "确定竞争优势和差异化方向",
                    "Specifics": "详细规划竞争策略",
                    "Persona": "考虑不同利益相关者的需求",
                    "Response": "制定行动计划和评估机制"
                },
                "variables": [
                    {
                        "name": "strategy_period",
                        "description": "策略周期",
                        "default": "短期/中期/长期"
                    }
                ],
                "target_role": '["产品经理"]',
                "order": 8
            }
        ]

        # 创建任务和关联模板
        tasks = [
            {
                "name": "竞品选择和市场定位分析",
                "description": "确定主要竞品并分析其市场定位",
                "template_name": "竞品分析框架"
            },
            {
                "name": "功能对比和评估",
                "description": "详细对比各竞品的功能特性并进行评估",
                "template_name": "功能对比矩阵生成"
            },
            {
                "name": "用户体验分析",
                "description": "评估各竞品的用户界面和使用体验",
                "template_name": "用户体验评估"
            },
            {
                "name": "价格策略和商业模式对比",
                "description": "分析竞品的定价策略和商业模式",
                "template_name": "定价策略分析"
            },
            {
                "name": "技术架构和扩展性分析",
                "description": "评估竞品的技术实现和扩展能力",
                "template_name": "技术架构评估"
            },
            {
                "name": "客户支持和服务评估",
                "description": "对比分析竞品的客户支持和服务质量",
                "template_name": "客户服务评估"
            },
            {
                "name": "SWOT分析",
                "description": "对主要竞品进行SWOT分析",
                "template_name": "SWOT分析"
            },
            {
                "name": "竞争策略制定",
                "description": "基于分析结果制定竞争策略",
                "template_name": "竞争策略制定"
            }
        ]

        # 创建所有模板
        for template_data in templates:
            if not Template.objects.filter(name=template_data["name"]).exists():
                Template.objects.create(
                    name=template_data["name"],
                    framework=template_data["framework"],
                    framework_type=template_data["framework_type"],
                    description=template_data["description"],
                    content=template_data["content"],
                    variables=template_data["variables"],
                    target_role=template_data["target_role"],
                    order=template_data["order"],
                    created_by=admin_user,
                    visibility='PUBLIC'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template_data["name"]}')
                )

        # 创建场景任务
        for task in tasks:
            template = Template.objects.get(name=task['template_name'])
            SceneTask.objects.create(
                scene=scene,
                name=task['name'],
                description=task['description'],
                template=template
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created task: {task["name"]}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created business analysis scene with all required templates')
        )