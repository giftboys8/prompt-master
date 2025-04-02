from django.core.management.base import BaseCommand
from frameworks.models import Framework, FrameworkModule

class Command(BaseCommand):
    help = '创建更多提示词框架：QUEST、POWER、FOCUS、CLEAR、RAPID'

    def handle(self, *args, **options):
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