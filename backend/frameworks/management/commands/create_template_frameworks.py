from django.core.management.base import BaseCommand
from frameworks.models import Framework, FrameworkModule

class Command(BaseCommand):
    help = '创建模板框架：SMART、CRISPR、PEAR、ALIGN、TASTE、COSTAR、DREAM'

    def handle(self, *args, **options):
        frameworks = [
            {
                'name': 'SMART框架',
                'description': 'Specific（具体）、Measurable（可衡量）、Achievable（可实现）、Relevant（相关性）、Time-bound（时限性）框架，用于设定清晰可执行的目标。',
                'modules': [
                    {'name': 'Specific', 'description': '具体 - 明确定义目标的具体内容', 'order': 1},
                    {'name': 'Measurable', 'description': '可衡量 - 设定可以量化的标准', 'order': 2},
                    {'name': 'Achievable', 'description': '可实现 - 确保目标在现有条件下可达成', 'order': 3},
                    {'name': 'Relevant', 'description': '相关性 - 确保目标与整体目标相关联', 'order': 4},
                    {'name': 'Time-bound', 'description': '时限性 - 设定明确的完成时间', 'order': 5}
                ]
            },
            {
                'name': 'CRISPR框架',
                'description': 'Context（上下文）、Request（请求）、Intent（意图）、Specifics（细节）、Persona（角色）、Response（响应）框架，用于构建精准的AI提示词。',
                'modules': [
                    {'name': 'Context', 'description': '上下文 - 提供必要的背景信息', 'order': 1},
                    {'name': 'Request', 'description': '请求 - 明确具体的需求', 'order': 2},
                    {'name': 'Intent', 'description': '意图 - 说明期望达成的目的', 'order': 3},
                    {'name': 'Specifics', 'description': '细节 - 补充具体的要求和限制', 'order': 4},
                    {'name': 'Persona', 'description': '角色 - 定义AI应扮演的角色', 'order': 5},
                    {'name': 'Response', 'description': '响应 - 期望的输出格式和结构', 'order': 6}
                ]
            },
            {
                'name': 'PEAR框架',
                'description': 'Purpose（目的）、Example（示例）、Action（行动）、Result（结果）框架，适用于任务导向的场景。',
                'modules': [
                    {'name': 'Purpose', 'description': '目的 - 明确任务的目标和意义', 'order': 1},
                    {'name': 'Example', 'description': '示例 - 提供参考案例或样本', 'order': 2},
                    {'name': 'Action', 'description': '行动 - 指定需要执行的具体步骤', 'order': 3},
                    {'name': 'Result', 'description': '结果 - 描述期望的输出形式', 'order': 4}
                ]
            },
            {
                'name': 'ALIGN框架',
                'description': 'Audience（受众）、Language（语言）、Intent（意图）、Goal（目标）、Need（需求）框架，适用于内容创作场景。',
                'modules': [
                    {'name': 'Audience', 'description': '受众 - 明确目标受众群体', 'order': 1},
                    {'name': 'Language', 'description': '语言 - 指定语言风格和表达方式', 'order': 2},
                    {'name': 'Intent', 'description': '意图 - 说明创作意图和目的', 'order': 3},
                    {'name': 'Goal', 'description': '目标 - 设定内容创作的目标', 'order': 4},
                    {'name': 'Need', 'description': '需求 - 明确内容需要满足的需求', 'order': 5}
                ]
            },
            {
                'name': 'TASTE框架',
                'description': 'Topic（主题）、Audience（受众）、Style（风格）、Tone（语气）、Extras（补充）框架，适用于文案写作场景。',
                'modules': [
                    {'name': 'Topic', 'description': '主题 - 确定写作的核心主题', 'order': 1},
                    {'name': 'Audience', 'description': '受众 - 定义目标读者群体', 'order': 2},
                    {'name': 'Style', 'description': '风格 - 指定写作风格', 'order': 3},
                    {'name': 'Tone', 'description': '语气 - 设定表达的语气', 'order': 4},
                    {'name': 'Extras', 'description': '补充 - 添加其他特殊要求', 'order': 5}
                ]
            },
            {
                'name': 'COSTAR框架',
                'description': 'Context（上下文）、Objective（目标）、Scope（范围）、Task（任务）、Action（行动）、Result（结果）框架，适用于项目规划场景。',
                'modules': [
                    {'name': 'Context', 'description': '上下文 - 提供项目背景信息', 'order': 1},
                    {'name': 'Objective', 'description': '目标 - 明确项目目标', 'order': 2},
                    {'name': 'Scope', 'description': '范围 - 界定项目范围', 'order': 3},
                    {'name': 'Task', 'description': '任务 - 分解具体任务', 'order': 4},
                    {'name': 'Action', 'description': '行动 - 规划执行步骤', 'order': 5},
                    {'name': 'Result', 'description': '结果 - 定义成功标准', 'order': 6}
                ]
            },
            {
                'name': 'DREAM框架',
                'description': 'Define（目标定义）、Reason（根因分析）、Explore（方案探索）、Adapt（调整实施）、Monitor（验证监控）框架，用于技术协作和系统性问题解决。',
                'modules': [
                    {'name': 'Define', 'description': '目标定义 - 明确系统边界和问题范围', 'order': 1},
                    {'name': 'Reason', 'description': '根因分析 - 定位问题本质和核心原因', 'order': 2},
                    {'name': 'Explore', 'description': '方案探索 - 生成并评估多个候选解决方案', 'order': 3},
                    {'name': 'Adapt', 'description': '调整实施 - 制定并实施代码级解决方案', 'order': 4},
                    {'name': 'Monitor', 'description': '验证监控 - 进行闭环测试和持续监控', 'order': 5}
                ]
            }
        ]

        for framework_data in frameworks:
            modules = framework_data.pop('modules')
            framework, created = Framework.objects.get_or_create(
                name=framework_data['name'],
                defaults=framework_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建{framework.name}'))
                
                # 创建框架的模块
                for module_data in modules:
                    FrameworkModule.objects.create(
                        framework=framework,
                        **module_data
                    )
                
                self.stdout.write(self.style.SUCCESS(f'成功创建{framework.name}的模块'))
            else:
                framework.description = framework_data['description']
                framework.save()
                self.stdout.write(self.style.SUCCESS(f'成功更新{framework.name}'))
                
                # 检查模块是否存在，不存在则创建
                if not framework.modules.exists():
                    for module_data in modules:
                        FrameworkModule.objects.create(
                            framework=framework,
                            **module_data
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'成功创建{framework.name}的模块'))