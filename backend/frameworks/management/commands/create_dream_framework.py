from django.core.management.base import BaseCommand
from frameworks.models import Framework, FrameworkModule

class Command(BaseCommand):
    help = '创建DREAM提示词框架，用于技术协作和问题解决'

    def handle(self, *args, **options):
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