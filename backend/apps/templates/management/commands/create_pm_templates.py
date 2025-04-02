from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = 'Create product manager core work templates'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID for template creation')

    def handle(self, *args, **options):
        user_id = options['user_id']
        user = User.objects.get(id=user_id)

        # 获取已存在的框架
        costar_framework = Framework.objects.get(name='COSTAR框架')
        rtgo_framework = Framework.objects.get(name='RTGO框架')
        smart_framework = Framework.objects.get(name='SMART框架')
        crispr_framework = Framework.objects.get(name='CRISPR框架')

        templates = [
            {
                "name": "产品需求文档(PRD)生成",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "基于COSTAR框架生成完整的产品需求文档，包含上下文、目标、范围、任务、行动和结果等关键要素",
                "content": {
                    "Context": "描述当前产品背景和市场环境，分析现有问题和痛点，收集用户研究数据和反馈",
                    "Objective": "明确产品目标和预期成果，设定可量化的成功指标（KPI），建立与业务目标的关联",
                    "Scope": "定义功能边界和项目交付范围，明确不包含的功能，制定MVP和迭代计划",
                    "Task": "列出详细功能需求，描述用户故事和场景，确定技术要求和性能指标",
                    "Action": "规划具体实现步骤，制定设计规范，设置测试要求和上线计划",
                    "Result": "预期的改进效果，业务指标提升预测，风险评估和成功标准"
                },
                "variables": [
                    {
                        "name": "feature_name",
                        "description": "功能名称",
                        "default": "待开发的功能或模块名称"
                    }
                ],
                "target_role": "产品经理",
                "order": 1
            },
            {
                "name": "用户故事地图构建",
                "framework": rtgo_framework,
                "framework_type": "RTGO框架",
                "description": "使用RTGO框架构建用户故事地图，明确角色、任务、目标和输出",
                "content": {
                    "Role": "定义目标用户角色和特征，分析用户背景、动机、需求和行为模式",
                    "Task": "识别用户需要完成的核心任务，进行优先级排序，分析任务依赖关系",
                    "Goal": "明确每个任务的目标，定义用户期望的结果，评估业务价值和意义",
                    "Output": "输出格式：\n1. 具体的功能需求\n2. 用户界面要求\n3. 交互流程设计\n4. 验收标准和指标"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待分析的产品名称"
                    }
                ],
                "target_role": "产品经理",
                "order": 2
            },
            {
                "name": "产品迭代规划",
                "framework": smart_framework,
                "framework_type": "SMART框架",
                "description": "使用SMART框架制定产品迭代计划，确保目标明确可执行",
                "content": {
                    "Specific": "明确本次迭代的具体目标，列出需要开发的功能和改进点",
                    "Measurable": "设定关键性能指标、用户体验指标、技术指标和业务指标",
                    "Achievable": "评估团队能力、资源可用性、技术可行性，制定风险应对措施",
                    "Relevant": "确保与产品战略、用户需求、市场趋势的一致性",
                    "Time-bound": "制定迭代周期规划，设定关键时间节点和里程碑"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待规划的产品名称"
                    },
                    {
                        "name": "iteration_period",
                        "description": "迭代周期",
                        "default": "迭代周期，如：Q1、Q2等"
                    }
                ],
                "target_role": "产品经理",
                "order": 3
            },
            {
                "name": "产品创新提案",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架生成产品创新提案，确保创意落地可执行",
                "content": {
                    "Context": "分析当前产品现状、市场环境、用户痛点和竞品情况",
                    "Request": "明确创新目标、待解决问题、业务预期和资源约束",
                    "Intent": "阐述创新的战略意义、用户价值和业务贡献",
                    "Specifics": "详细说明创新点，分析技术可行性，评估资源需求",
                    "Persona": "描绘目标用户画像，定义用户场景和价值主张",
                    "Response": "制定执行计划，评估风险，设定成功指标"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待创新的产品名称"
                    }
                ],
                "target_role": "产品经理",
                "order": 4
            },
            {
                "name": "产品竞品分析",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架进行深度竞品分析，发现差异化机会",
                "content": {
                    "Context": "收集竞品基本信息、市场地位、发展历史和商业模式",
                    "Request": "确定分析目标、重点关注领域和数据来源",
                    "Intent": "解读竞品战略、产品定位和核心竞争力",
                    "Specifics": "进行功能对比、用户体验评估和技术架构分析",
                    "Persona": "对比用户群体，分析用户评价和忠诚度",
                    "Response": "总结优劣势，提供差异化建议和竞争策略"
                },
                "variables": [
                    {
                        "name": "competitor_name",
                        "description": "竞品名称",
                        "default": "待分析的竞品名称"
                    }
                ],
                "target_role": "产品经理",
                "order": 5
            },
            {
                "name": "产品路线图规划",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架制定产品路线图，确保产品演进方向清晰",
                "content": {
                    "Context": "评估产品当前状态，分析市场趋势和竞争格局",
                    "Objective": "确定产品愿景和战略目标，明确业务和技术目标",
                    "Scope": "规划产品演进范围、技术架构和功能模块",
                    "Task": "制定功能迭代、技术升级和性能优化计划",
                    "Action": "规划实施步骤、资源分配和里程碑",
                    "Result": "设定预期目标、关键指标和评估方法"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待规划的产品名称"
                    },
                    {
                        "name": "time_period",
                        "description": "规划周期",
                        "default": "规划周期，如：2024年、2024-2025等"
                    }
                ],
                "target_role": "产品经理",
                "order": 6
            }
        ]

        for template_data in templates:
            template = Template.objects.create(
                name=template_data["name"],
                framework=template_data["framework"],
                framework_type=template_data["framework_type"],
                description=template_data["description"],
                content=template_data["content"],
                variables=template_data["variables"],
                target_role=template_data["target_role"],
                order=template_data["order"],
                created_by=user,
                visibility='PUBLIC'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created template: {template.name}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Description: {template.description}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(templates)} product manager templates')
        )