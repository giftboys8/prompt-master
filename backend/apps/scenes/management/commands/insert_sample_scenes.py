from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.scenes.models import Scene, SceneTask
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Insert sample scenes and tasks into the database'

    def handle(self, *args, **options):
        # 确保有一个超级用户
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR('No superuser found. Please create a superuser first.'))
            return

        # 创建示例场景
        scene, created = Scene.objects.get_or_create(
            name="产品需求分析",
            defaults={
                "category": "产品管理",
                "description": "分析产品需求并生成详细报告",
                "target_roles": ["产品经理", "业务分析师"],
                "status": True,
                "created_by": superuser,
                "version": "1.0.0"
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created scene: {scene.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Scene "{scene.name}" already exists'))

        # 为场景创建任务
        tasks = [
            {
                "name": "收集用户反馈",
                "description": "从各个渠道收集用户对产品的反馈"
            },
            {
                "name": "分析市场趋势",
                "description": "研究当前市场趋势和竞品情况"
            },
            {
                "name": "制定需求文档",
                "description": "根据收集的信息制定详细的产品需求文档"
            }
        ]

        for task_data in tasks:
            task, task_created = SceneTask.objects.get_or_create(
                scene=scene,
                name=task_data['name'],
                defaults={
                    "description": task_data['description']
                }
            )

            if task_created:
                self.stdout.write(self.style.SUCCESS(f'Created task: {task.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Task "{task.name}" already exists'))

        self.stdout.write(self.style.SUCCESS('Sample data insertion completed'))