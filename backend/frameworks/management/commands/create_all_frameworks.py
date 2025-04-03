from django.core.management.base import BaseCommand
from frameworks.models import Framework, FrameworkModule

class Command(BaseCommand):
    help = '创建所有提示词框架'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始创建所有提示词框架...'))
        
        # 创建RTGO框架 (from create_default_frameworks.py)
        self._create_rtgo_framework()
        
        # 创建DREAM框架 (from create_dream_framework.py)
        self._create_dream_framework()
        
        # 创建模板框架：SMART、CRISPR、PEAR、ALIGN、TASTE、COSTAR (from create_template_frameworks.py)
        self._create_template_frameworks()
        
        # 创建更多框架：QUEST、POWER、FOCUS、CLEAR、RAPID (from create_more_frameworks.py)
        self._create_more_frameworks()
        
        self.stdout.write(self.style.SUCCESS('所有提示词框架创建完成!'))

    def _create_framework(self, framework_data):
        """通用框架创建方法"""
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
            existing_modules = set(framework.modules.values_list('name', flat=True))
            for module_data in modules:
                if module_data['name'] not in existing_modules:
                    FrameworkModule.objects.create(
                        framework=framework,
                        **module_data
                    )
            
            self.stdout.write(self.style.SUCCESS(f'成功更新{framework.name}的模块'))
        
        return framework

    def _create_rtgo_framework(self):
        """创建RTGO框架"""
        self.stdout.write('创建RTGO框架...')
        framework_data = {
            'name': 'RTGO框架',
            'description': 'Role-Task-Goal-Output框架，适用于角色导向的任务执行场景。',
            'modules': [
                {'name': 'Role', 'description': '角色定义 - 定义AI应扮演的角色', 'order': 1},
                {'name': 'Task', 'description': '任务描述 - 描述AI需要执行的任务', 'order': 2},
                {'name': 'Goal', 'description': '目标设定 - 明确任务的目标和期望结果', 'order': 3},
                {'name': 'Output', 'description': '输出格式 - 指定AI回复的格式和结构', 'order': 4}
            ]
        }
        self._create_framework(framework_data)

    def _create_dream_framework(self):
        """创建DREAM框架"""
        self.stdout.write('创建DREAM框架...')
        framework_data = {
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
        self._create_framework(framework_data)

    def _create_template_frameworks(self):
        """创建模板框架：SMART、CRISPR、PEAR、ALIGN、TASTE、COSTAR"""
        self.stdout.write('创建模板框架：SMART、CRISPR、PEAR、ALIGN、TASTE、COSTAR...')
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
                    {'name': 'Example', 'description': '示例 - 提供参考案例', 'order': 2},
                    {'name': 'Action', 'description': '行动 - 说明需要执行的具体步骤', 'order': 3},
                    {'name': 'Result', 'description': '结果 - 描述期望的输出结果', 'order': 4}
                ]
            },
            {
                'name': 'ALIGN框架',
                'description': 'Audience（受众）、Language（语言）、Intent（意图）、Goal（目标）、Narrative（叙述）框架，适用于内容创作场景。',
                'modules': [
                    {'name': 'Audience', 'description': '受众 - 确定内容的目标受众', 'order': 1},
                    {'name': 'Language', 'description': '语言 - 定义内容的语言风格和语调', 'order': 2},
                    {'name': 'Intent', 'description': '意图 - 明确内容的目的和意图', 'order': 3},
                    {'name': 'Goal', 'description': '目标 - 设定内容需要达成的目标', 'order': 4},
                    {'name': 'Narrative', 'description': '叙述 - 构建内容的叙述结构', 'order': 5}
                ]
            },
            {
                'name': 'TASTE框架',
                'description': 'Topic（主题）、Audience（受众）、Style（风格）、Tone（语调）、Extras（附加要求）框架，适用于创意写作场景。',
                'modules': [
                    {'name': 'Topic', 'description': '主题 - 确定写作的主题和内容', 'order': 1},
                    {'name': 'Audience', 'description': '受众 - 明确目标读者群体', 'order': 2},
                    {'name': 'Style', 'description': '风格 - 定义写作的风格和形式', 'order': 3},
                    {'name': 'Tone', 'description': '语调 - 设定写作的语气和情感基调', 'order': 4},
                    {'name': 'Extras', 'description': '附加要求 - 补充其他特殊要求', 'order': 5}
                ]
            },
            {
                'name': 'COSTAR框架',
                'description': 'Context（上下文）、Objective（目标）、Scope（范围）、Target audience（目标受众）、Action items（行动项）、Requirements（要求）框架，适用于项目规划场景。',
                'modules': [
                    {'name': 'Context', 'description': '上下文 - 提供项目的背景信息', 'order': 1},
                    {'name': 'Objective', 'description': '目标 - 明确项目的目标', 'order': 2},
                    {'name': 'Scope', 'description': '范围 - 定义项目的边界和范围', 'order': 3},
                    {'name': 'Target audience', 'description': '目标受众 - 确定项目的受众群体', 'order': 4},
                    {'name': 'Action items', 'description': '行动项 - 列出需要执行的具体任务', 'order': 5},
                    {'name': 'Requirements', 'description': '要求 - 说明项目的特殊要求和限制', 'order': 6}
                ]
            }
        ]

        for framework_data in frameworks:
            self._create_framework(framework_data)

    def _create_more_frameworks(self):
        """创建更多框架：QUEST、POWER、FOCUS、CLEAR、RAPID"""
        self.stdout.write('创建更多框架：QUEST、POWER、FOCUS、CLEAR、RAPID...')
        frameworks = [
            {
                'name': 'QUEST框架',
                'description': 'Question（问题）、Understand（理解）、Explore（探索）、Solve（解决）、Test（测试）框架，适用于问题解决和调试场景。',
                'modules': [
                    {'name': 'Question', 'description': '问题 - 准确描述待解决的问题', 'order': 1},
                    {'name': 'Understand', 'description': '理解 - 深入理解问题的上下文和影响', 'order': 2},
                    {'name': 'Explore', 'description': '探索 - 研究可能的解决方案', 'order': 3},
                    {'name': 'Solve', 'description': '解决 - 实施最佳解决方案', 'order': 4},
                    {'name': 'Test', 'description': '测试 - 验证解决方案的有效性', 'order': 5}
                ]
            },
            {
                'name': 'POWER框架',
                'description': 'Purpose（目标）、Options（选项）、Weigh（权衡）、Execute（执行）、Review（回顾）框架，适用于决策制定场景。',
                'modules': [
                    {'name': 'Purpose', 'description': '目标 - 明确决策的目的和期望结果', 'order': 1},
                    {'name': 'Options', 'description': '选项 - 列举所有可能的选择', 'order': 2},
                    {'name': 'Weigh', 'description': '权衡 - 评估各个选项的利弊', 'order': 3},
                    {'name': 'Execute', 'description': '执行 - 实施选定的方案', 'order': 4},
                    {'name': 'Review', 'description': '回顾 - 评估决策的结果和影响', 'order': 5}
                ]
            },
            {
                'name': 'FOCUS框架',
                'description': 'Facts（事实）、Objectives（目标）、Challenges（挑战）、Understanding（理解）、Solution（解决方案）框架，适用于分析和规划场景。',
                'modules': [
                    {'name': 'Facts', 'description': '事实 - 收集相关的客观事实', 'order': 1},
                    {'name': 'Objectives', 'description': '目标 - 确定需要达成的目标', 'order': 2},
                    {'name': 'Challenges', 'description': '挑战 - 识别潜在的障碍和风险', 'order': 3},
                    {'name': 'Understanding', 'description': '理解 - 深入理解问题和环境', 'order': 4},
                    {'name': 'Solution', 'description': '解决方案 - 制定完整的解决方案', 'order': 5}
                ]
            },
            {
                'name': 'CLEAR框架',
                'description': 'Context（上下文）、Logic（逻辑）、Example（示例）、Action（行动）、Result（结果）框架，适用于知识传递和教学场景。',
                'modules': [
                    {'name': 'Context', 'description': '上下文 - 提供必要的背景信息', 'order': 1},
                    {'name': 'Logic', 'description': '逻辑 - 解释原理和思路', 'order': 2},
                    {'name': 'Example', 'description': '示例 - 提供具体的例子', 'order': 3},
                    {'name': 'Action', 'description': '行动 - 说明实践步骤', 'order': 4},
                    {'name': 'Result', 'description': '结果 - 描述预期的学习成果', 'order': 5}
                ]
            },
            {
                'name': 'RAPID框架',
                'description': 'Review（审查）、Analyze（分析）、Plan（计划）、Implement（实施）、Document（文档）框架，适用于快速迭代和开发场景。',
                'modules': [
                    {'name': 'Review', 'description': '审查 - 快速评估当前状况', 'order': 1},
                    {'name': 'Analyze', 'description': '分析 - 分析问题和需求', 'order': 2},
                    {'name': 'Plan', 'description': '计划 - 制定行动计划', 'order': 3},
                    {'name': 'Implement', 'description': '实施 - 执行开发任务', 'order': 4},
                    {'name': 'Document', 'description': '文档 - 记录过程和结果', 'order': 5}
                ]
            }
        ]

        for framework_data in frameworks:
            self._create_framework(framework_data)