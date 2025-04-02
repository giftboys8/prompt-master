from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = 'Create product operation expert core work templates'

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
                "name": "用户增长策略规划",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "基于COSTAR框架制定用户增长策略，包含市场分析、目标设定、策略规划、执行方案和效果评估等关键要素",
                "content": {
                    "Context": "分析当前用户增长现状、市场环境、竞品情况和目标用户特征",
                    "Objective": "设定用户增长目标，包括新用户获取、用户活跃度、留存率等关键指标",
                    "Scope": "确定增长策略范围，包括获客渠道、用户触达方式、活动形式等",
                    "Task": "制定具体的增长任务，包括渠道投放、内容营销、活动策划等",
                    "Action": "详细的执行计划，包括资源分配、时间节点、团队分工等",
                    "Result": "预期效果评估，包括ROI分析、用户生命周期价值预测等"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待增长的产品名称"
                    },
                    {
                        "name": "target_period",
                        "description": "目标周期",
                        "default": "增长目标周期，如：Q3、2024H1等"
                    }
                ],
                "target_role": "产品运营",
                "order": 1
            },
            {
                "name": "用户运营活动策划",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架设计用户运营活动，确保活动效果和用户参与度",
                "content": {
                    "Context": "分析活动背景、用户需求、历史活动数据和市场动态",
                    "Request": "明确活动目标、预算限制、效果预期和关键指标",
                    "Intent": "确定活动主题、价值主张和用户利益点",
                    "Specifics": "详细设计活动机制、奖励方案、玩法规则等",
                    "Persona": "细分目标用户群体，设计差异化的参与方案",
                    "Response": "制定活动执行计划、风险预案和效果评估方案"
                },
                "variables": [
                    {
                        "name": "activity_name",
                        "description": "活动名称",
                        "default": "待策划的活动名称"
                    },
                    {
                        "name": "activity_period",
                        "description": "活动周期",
                        "default": "活动持续时间"
                    }
                ],
                "target_role": "产品运营",
                "order": 2
            },
            {
                "name": "用户留存方案设计",
                "framework": rtgo_framework,
                "framework_type": "RTGO框架",
                "description": "使用RTGO框架设计用户留存方案，提升产品的用户粘性和活跃度",
                "content": {
                    "Role": "分析不同用户角色的使用习惯、流失原因和需求特点",
                    "Task": "设计针对性的留存策略，包括产品优化、用户激励等任务",
                    "Goal": "设定留存率目标，分阶段的提升计划和效果预期",
                    "Output": "输出具体执行方案：\\n1. 产品功能优化建议\\n2. 用户激励机制\\n3. 内容运营策略\\n4. 社区运营方案"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待优化的产品名称"
                    }
                ],
                "target_role": "产品运营",
                "order": 3
            },
            {
                "name": "数据分析报告生成",
                "framework": smart_framework,
                "framework_type": "SMART框架",
                "description": "使用SMART框架生成数据分析报告，深入洞察用户行为和产品性能",
                "content": {
                    "Specific": "明确分析目标和关注指标，确定数据维度和分析方向",
                    "Measurable": "设定具体的数据指标，包括用户行为、转化率、留存率等",
                    "Achievable": "确保数据可获取性，制定数据收集和处理方案",
                    "Relevant": "关联业务目标，确保分析结果对决策有指导意义",
                    "Time-bound": "设定分析周期，确定报告频率和时间节点"
                },
                "variables": [
                    {
                        "name": "report_type",
                        "description": "报告类型",
                        "default": "日报/周报/月报/季报"
                    },
                    {
                        "name": "analysis_period",
                        "description": "分析周期",
                        "default": "待分析的时间段"
                    }
                ],
                "target_role": "产品运营",
                "order": 4
            },
            {
                "name": "用户反馈分析与优化",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架分析用户反馈并制定产品优化方案",
                "content": {
                    "Context": "收集用户反馈渠道、反馈类型和历史处理情况",
                    "Request": "确定分析目标、优先级标准和处理流程",
                    "Intent": "理解用户真实需求和痛点，识别核心问题",
                    "Specifics": "分类整理反馈内容，提出具体优化建议",
                    "Persona": "结合用户画像分析反馈代表性和普遍性",
                    "Response": "制定优化方案，设定改进计划和效果跟踪"
                },
                "variables": [
                    {
                        "name": "feedback_source",
                        "description": "反馈来源",
                        "default": "用户反馈的收集渠道"
                    }
                ],
                "target_role": "产品运营",
                "order": 5
            },
            {
                "name": "产品生命周期运营",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架制定产品全生命周期运营策略",
                "content": {
                    "Context": "分析产品所处生命周期阶段、市场地位和竞争态势",
                    "Objective": "制定阶段性运营目标，包括用户规模、收入等指标",
                    "Scope": "确定运营策略范围，包括用户运营、内容运营、活动运营等",
                    "Task": "设计针对性的运营任务，制定资源投入计划",
                    "Action": "详细的执行方案，包括团队分工、时间节点等",
                    "Result": "预期效果评估，包括各阶段KPI和里程碑"
                },
                "variables": [
                    {
                        "name": "product_name",
                        "description": "产品名称",
                        "default": "待运营的产品名称"
                    },
                    {
                        "name": "lifecycle_stage",
                        "description": "生命周期阶段",
                        "default": "导入期/成长期/成熟期/衰退期"
                    }
                ],
                "target_role": "产品运营",
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
            self.style.SUCCESS(f'Successfully created {len(templates)} product operation templates')
        )