from django.db import migrations
import json

def fix_target_roles(apps, schema_editor):
    Scene = apps.get_model('scenes', 'Scene')
    for scene in Scene.objects.all():
        # 确保target_roles是一个列表
        if not isinstance(scene.target_roles, list):
            try:
                if isinstance(scene.target_roles, str):
                    # 尝试解析JSON字符串
                    if scene.target_roles.startswith('[') and scene.target_roles.endswith(']'):
                        try:
                            parsed = json.loads(scene.target_roles)
                            if isinstance(parsed, list):
                                scene.target_roles = parsed
                            else:
                                scene.target_roles = [str(parsed)]
                        except json.JSONDecodeError:
                            # 如果解析失败，将整个字符串作为一个元素
                            scene.target_roles = [scene.target_roles]
                    else:
                        # 普通字符串直接作为一个元素
                        scene.target_roles = [scene.target_roles]
                else:
                    # 其他类型转换为字符串后作为一个元素
                    scene.target_roles = [str(scene.target_roles)]
            except Exception as e:
                print(f"处理场景 {scene.id} 时出错: {str(e)}")
                scene.target_roles = []

        # 确保数组中的每个元素都是字符串
        scene.target_roles = [
            str(role).strip() if isinstance(role, (str, int, float))
            else role[0] if isinstance(role, list) and len(role) > 0
            else str(role)
            for role in scene.target_roles
            if role is not None and str(role).strip()
        ]
        
        # 移除重复项
        scene.target_roles = list(dict.fromkeys(scene.target_roles))
        
        scene.save()

class Migration(migrations.Migration):
    dependencies = [
        ('scenes', '0004_update_target_roles_data'),
    ]

    operations = [
        migrations.RunPython(fix_target_roles, migrations.RunPython.noop),
    ]