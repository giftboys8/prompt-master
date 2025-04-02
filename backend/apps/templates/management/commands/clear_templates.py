from django.core.management.base import BaseCommand
from apps.templates.models import Template, TemplateVersion, SharedTemplate, TemplateTest

class Command(BaseCommand):
    help = '清除所有提示词模板相关的数据'

    def handle(self, *args, **options):
        # 首先删除相关的记录
        self.stdout.write('开始删除模板测试记录...')
        test_count = TemplateTest.objects.all().count()
        TemplateTest.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'成功删除 {test_count} 条测试记录'))

        self.stdout.write('开始删除模板分享记录...')
        share_count = SharedTemplate.objects.all().count()
        SharedTemplate.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'成功删除 {share_count} 条分享记录'))

        self.stdout.write('开始删除模板版本记录...')
        version_count = TemplateVersion.objects.all().count()
        TemplateVersion.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'成功删除 {version_count} 条版本记录'))

        self.stdout.write('开始删除模板记录...')
        template_count = Template.objects.all().count()
        Template.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'成功删除 {template_count} 条模板记录'))

        self.stdout.write(self.style.SUCCESS('所有提示词模板相关数据已清除'))