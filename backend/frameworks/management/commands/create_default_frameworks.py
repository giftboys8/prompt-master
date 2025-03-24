from django.core.management.base import BaseCommand
from frameworks.models import Framework, FrameworkModule

class Command(BaseCommand):
    help = '创建默认的提示词框架'

    def handle(self, *args, **options):
        # 创建RTGO框架
        rtgo_framework, created = Framework.objects.get_or_create(
            name='RTGO框架',
            defaults={
                'description': 'Role-Task-Goal-Output框架，适用于角色导向的任务执行场景。'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('成功创建RTGO框架'))
            
            # 创建RTGO框架的模块
            modules = [
                {
                    'name': 'Role',
                    'description': '角色定义 - 定义AI应扮演的角色',
                    'order': 1
                },
                {
                    'name': 'Task',
                    'description': '任务描述 - 描述AI需要执行的任务',
                    'order': 2
                },
                {
                    'name': 'Goal',
                    'description': '目标设定 - 明确任务的目标和期望结果',
                    'order': 3
                },
                {
                    'name': 'Output',
                    'description': '输出格式 - 指定AI回复的格式和结构',
                    'order': 4
                }
            ]
            
            for module_data in modules:
                FrameworkModule.objects.create(
                    framework=rtgo_framework,
                    **module_data
                )
            
            self.stdout.write(self.style.SUCCESS('成功创建RTGO框架的模块'))
        else:
            rtgo_framework.description = 'Role-Task-Goal-Output框架，适用于角色导向的任务执行场景。'
            rtgo_framework.save()
            self.stdout.write(self.style.SUCCESS('成功更新RTGO框架'))
            
            # 检查模块是否存在，不存在则创建
            if not rtgo_framework.modules.exists():
                modules = [
                    {
                        'name': 'Role',
                        'description': '角色定义 - 定义AI应扮演的角色',
                        'order': 1
                    },
                    {
                        'name': 'Task',
                        'description': '任务描述 - 描述AI需要执行的任务',
                        'order': 2
                    },
                    {
                        'name': 'Goal',
                        'description': '目标设定 - 明确任务的目标和期望结果',
                        'order': 3
                    },
                    {
                        'name': 'Output',
                        'description': '输出格式 - 指定AI回复的格式和结构',
                        'order': 4
                    }
                ]
                
                for module_data in modules:
                    FrameworkModule.objects.create(
                        framework=rtgo_framework,
                        **module_data
                    )
                
                self.stdout.write(self.style.SUCCESS('成功创建RTGO框架的模块'))