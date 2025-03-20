from django.core.management.base import BaseCommand
from apps.templates.models import Template

class Command(BaseCommand):
    help = '更新产品经理模板的使用角色字段'

    def handle(self, *args, **kwargs):
        # 定义产品经理模板角色映射
        role_mapping = {
            'A/B测试方案设计': '产品经理、数据分析师、增长黑客',
            '产品PRD文档生成器': '产品经理、产品设计师、需求分析师',
            '用户故事与场景设计': '产品经理、用户体验设计师、需求分析师',
            '竞品分析专家': '产品经理、市场分析师、战略规划师',
            '产品规划路线图制定': '产品经理、项目经理、战略规划师',
            '用户需求分析专家': '产品经理、用户研究员、需求分析师',
        }

        # 更新模板角色
        updated_count = 0
        for template in Template.objects.filter(name__in=role_mapping.keys()):
            template.target_role = role_mapping[template.name]
            template.save()
            updated_count += 1
            self.stdout.write(f'已更新模板 "{template.name}" 的角色为：{template.target_role}')

        self.stdout.write(
            self.style.SUCCESS(
                f'成功更新了 {updated_count} 个产品经理模板的使用角色！'
            )
        )