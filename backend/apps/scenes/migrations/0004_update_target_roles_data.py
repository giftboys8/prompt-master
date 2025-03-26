from django.db import migrations
import json

def convert_target_roles(apps, schema_editor):
    Scene = apps.get_model('scenes', 'Scene')
    for scene in Scene.objects.all():
        if isinstance(scene.target_roles, str):
            try:
                # 尝试解析 JSON 字符串
                roles = json.loads(scene.target_roles)
                if isinstance(roles, list):
                    scene.target_roles = roles
                else:
                    scene.target_roles = [str(roles)]
            except json.JSONDecodeError:
                # 如果不是有效的 JSON，将其作为单个角色
                scene.target_roles = [scene.target_roles]
            scene.save()

class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0003_remove_scenetask_applicable_roles'),
    ]

    operations = [
        migrations.RunPython(convert_target_roles, migrations.RunPython.noop),
    ]