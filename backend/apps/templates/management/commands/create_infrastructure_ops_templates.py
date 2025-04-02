from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = 'Create infrastructure operations expert core work templates'

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
                "target_role": "基础设施运维",
                "order": 1
            },
            {
                "name": "故障排查和根因分析",
                "framework": crispr_framework,
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
                "target_role": "基础设施运维",
                "order": 2
            },
            {
                "name": "容量规划和资源优化",
                "framework": smart_framework,
                "framework_type": "SMART框架",
                "description": "使用SMART框架进行基础设施容量规划和资源优化，提高资源利用效率",
                "content": {
                    "Specific": "明确规划目标，包括计算、存储、网络等资源需求",
                    "Measurable": "设定具体的容量指标，如CPU使用率、内存占用、存储容量等",
                    "Achievable": "评估现有资源和扩展可能性，制定可行的优化方案",
                    "Relevant": "确保规划与业务增长和技术演进相关联",
                    "Time-bound": "制定分阶段的实施计划和里程碑"
                },
                "variables": [
                    {
                        "name": "planning_period",
                        "description": "规划周期",
                        "default": "短期（3个月）/中期（6-12个月）/长期（1-3年）"
                    },
                    {
                        "name": "growth_rate",
                        "description": "预期增长率",
                        "default": "年度增长百分比"
                    }
                ],
                "target_role": "基础设施运维",
                "order": 3
            },
            {
                "name": "自动化运维流程设计",
                "framework": rtgo_framework,
                "framework_type": "RTGO框架",
                "description": "使用RTGO框架设计自动化运维流程，提高运维效率和一致性",
                "content": {
                    "Role": "定义自动化运维的目标角色和受益方",
                    "Task": "识别可自动化的运维任务，如部署、配置管理、监控等",
                    "Goal": "设定自动化目标，包括效率提升、错误减少、一致性增强等",
                    "Output": "输出自动化方案：\\n1. 工具选型和集成方案\\n2. 脚本和配置模板\\n3. CI/CD流程设计\\n4. 自动化测试策略"
                },
                "variables": [
                    {
                        "name": "automation_scope",
                        "description": "自动化范围",
                        "default": "部署/配置管理/监控/备份恢复"
                    },
                    {
                        "name": "tech_stack",
                        "description": "技术栈",
                        "default": "使用的主要技术和工具"
                    }
                ],
                "target_role": "基础设施运维",
                "order": 4
            },
            {
                "name": "灾备和业务连续性规划",
                "framework": costar_framework,
                "framework_type": "COSTAR框架",
                "description": "使用COSTAR框架制定全面的灾备和业务连续性计划，确保关键业务的持续运行",
                "content": {
                    "Context": "分析当前基础设施和业务的关键依赖",
                    "Objective": "设定灾备目标，包括恢复时间目标（RTO）和恢复点目标（RPO）",
                    "Scope": "确定需要保护的关键系统和数据",
                    "Task": "制定具体的灾备任务，包括备份策略、故障转移机制等",
                    "Action": "详细的实施计划，包括技术方案、演练计划、团队职责等",
                    "Result": "预期效果评估，包括系统可用性提升、潜在损失减少等"
                },
                "variables": [
                    {
                        "name": "business_criticality",
                        "description": "业务关键程度",
                        "default": "低/中/高/极高"
                    },
                    {
                        "name": "geo_distribution",
                        "description": "地理分布",
                        "default": "单一地点/多地区/全球"
                    }
                ],
                "target_role": "基础设施运维",
                "order": 5
            },
            {
                "name": "安全加固和合规性检查",
                "framework": crispr_framework,
                "framework_type": "CRISPR框架",
                "description": "使用CRISPR框架进行基础设施安全加固和合规性检查，提高系统安全性",
                "content": {
                    "Context": "分析当前安全状况、威胁景观和适用的合规要求",
                    "Request": "明确安全加固目标和合规检查范围",
                    "Intent": "识别潜在的安全漏洞和合规性缺口",
                    "Specifics": "详细的安全加固措施和合规性检查清单",
                    "Persona": "确定相关的安全团队和合规官员",
                    "Response": "制定实施计划、风险缓解策略和持续改进方案"
                },
                "variables": [
                    {
                        "name": "security_level",
                        "description": "安全等级要求",
                        "default": "基础/高级/金融级/军工级"
                    },
                    {
                        "name": "compliance_standards",
                        "description": "适用的合规标准",
                        "default": "ISO27001/PCI DSS/GDPR/等"
                    }
                ],
                "target_role": "基础设施运维",
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
            self.style.SUCCESS(f'Successfully created {len(templates)} infrastructure operations templates')
        )