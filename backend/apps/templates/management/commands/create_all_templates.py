from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = 'Create all core work templates for product managers, product operations, and infrastructure operations'

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
            # Product Manager Templates
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
                "target_role": '["产品经理"]',
                "order": 1
            },
            # ... (其他产品经理模板)

            # Product Operation Templates
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
                "target_role": '["产品运营"]',
                "order": 7
            },
            # ... (其他产品运营模板)

            # Infrastructure Operations Templates
            {
                "name": "基础设施监控方案设计",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架设计全面的基础设施监控方案，确保系统稳定性和性能",
                "content": {
                    "Context": "分析当前基础设施状况、业务需求和技术栈",
                    "Objective": "设定监控目标，包括可用性、性能指标和告警阈值",
                    "Scope": "确定监控范围，包括服务器、网络设备、应用服务等",
                    "Task": "制定具体监控任务，包括指标收集、日志分析、告警设置等",
                    "Action": "详细的实施计划，包括工具选型、部署步骤、团队分工等",
                    "Result": "预期效果评估，包括监控覆盖率、响应时间改善等"
                },
                "variables": [
                    {
                        "name": "infrastructure_type",
                        "description": "基础设施类型",
                        "default": "云服务/本地数据中心/混合环境"
                    },
                    {
                        "name": "scale",
                        "description": "规模",
                        "default": "服务器数量或业务规模"
                    }
                ],
                "target_role": '["基础设施运维"]',
                "order": 13
            },
            # ... (其他基础设施运维模板)
        ]

        # 添加所有产品经理模板
        templates.extend(self._get_product_manager_templates())
        
        # 添加所有产品运营模板
        templates.extend(self._get_product_operation_templates())
        
        # 添加所有基础设施运维模板
        templates.extend(self._get_infrastructure_ops_templates())

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
            self.style.SUCCESS(f'Successfully created {len(templates)} templates')
        )

    def _get_product_manager_templates(self):
        # 从create_pm_templates.py中获取产品经理模板
        # 这里只列出了一个示例，实际应包含所有产品经理模板
        return [
            {
                "name": "用户故事地图构建",
                "framework": Framework.objects.get(name='RTGO框架'),
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
                "target_role": '["产品经理"]',
                "order": 2
            },
            # 添加其他产品经理模板...
        ]

    def _get_product_operation_templates(self):
        # 从create_operation_templates.py中获取产品运营模板
        # 这里只列出了一个示例，实际应包含所有产品运营模板
        return [
            {
                "name": "用户运营活动策划",
                "framework": Framework.objects.get(name='CRISPR框架'),
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
                "target_role": '["产品运营"]',
                "order": 8
            },
            # 添加其他产品运营模板...
        ]

    def _get_infrastructure_ops_templates(self):
        # 从create_infrastructure_ops_templates.py中获取基础设施运维模板
        # 这里只列出了一个示例，实际应包含所有基础设施运维模板
        return [
            {
                "name": "故障排查和根因分析",
                "framework": Framework.objects.get(name='CRISPR框架'),
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架进行系统故障排查和根因分析，提高问题解决效率",
                "content": {
                    "Context": "收集故障现象、影响范围和初步诊断信息",
                    "Request": "明确排查目标、优先级和时间限制",
                    "Intent": "分析可能的故障原因和影响因素",
                    "Specifics": "详细的排查步骤，包括日志分析、性能诊断、网络追踪等",
                    "Persona": "确定需要协作的团队和角色",
                    "Response": "制定修复方案、预防措施和复盘报告"
                },
                "variables": [
                    {
                        "name": "issue_type",
                        "description": "故障类型",
                        "default": "服务中断/性能下降/数据异常"
                    },
                    {
                        "name": "severity",
                        "description": "严重程度",
                        "default": "低/中/高/紧急"
                    }
                ],
                "target_role": '["基础设施运维"]',
                "order": 14
            },
            # 添加其他基础设施运维模板...
        ]