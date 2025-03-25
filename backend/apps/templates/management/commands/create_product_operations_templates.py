from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.product_operations_templates import create_product_operations_templates

User = get_user_model()

class Command(BaseCommand):
    help = '创建产品运营经理提示词模板'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='创建模板的用户ID')

    def handle(self, *args, **options):
        user_id = options['user_id']
        try:
            user = User.objects.get(id=user_id)
            create_product_operations_templates(user_id)
            self.stdout.write(self.style.SUCCESS(f'成功为用户 {user.username} 创建产品运营经理提示词模板'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'用户ID {user_id} 不存在'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'创建模板失败: {str(e)}'))