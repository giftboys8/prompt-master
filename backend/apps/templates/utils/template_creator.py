from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template
from django.core.management.base import CommandError

User = get_user_model()

def create_db_ops_templates(user_id):
    """
    创建数据库运维工程师的提示词模板
    :param user_id: 创建模板的用户ID
    :return: tuple (created_count: int, message: str)
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise CommandError(f'用户ID {user_id} 不存在')

    # 使用COSTAR框架
    framework, created = Framework.objects.get_or_create(
        name='COSTAR',
        defaults={
            'description': 'Context（上下文）、Objective（目标）、Scope（范围）、Task（任务）、Action（行动）、Result（结果）框架，适用于项目规划场景。'
        }
    )

    # 从create_db_ops_templates.py导入模板定义
    from apps.templates.management.commands.create_db_ops_templates import Command as TemplateCommand
    template_command = TemplateCommand()
    templates = template_command.templates

    created_count = 0
    for template_data in templates:
        # 检查模板是否已存在
        existing = Template.objects.filter(
            name=template_data["name"],
            target_role=template_data["target_role"]
        ).exists()
        
        if not existing:
            Template.objects.create(
                name=template_data["name"],
                framework=framework,
                framework_type=framework.name,
                description=template_data["description"],
                content=template_data["content"],
                variables=template_data["variables"],
                target_role=template_data["target_role"],
                created_by=user,
                visibility='PUBLIC'  # 设置为公开可见
            )
            created_count += 1

    return created_count, f'成功创建 {created_count} 个数据库运维工程师模板'