# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0007_alter_templatetest_model'),
        ('frameworks', '0002_framework_created_by'),
    ]

    operations = [
        # 移除 0006 中添加的 framework 字段
        migrations.RemoveField(
            model_name='template',
            name='framework',
        ),
        migrations.RemoveField(
            model_name='templateversion',
            name='framework',
        ),
        # 恢复 0002 中移除的 framework_type 字段
        migrations.AddField(
            model_name='template',
            name='framework_type',
            field=models.CharField(
                choices=[
                    ("RTGO", "RTGO"),
                    ("SPAR", "SPAR"),
                    ("CUSTOM", "Custom"),
                ],
                max_length=10,
                verbose_name="框架类型",
                default="CUSTOM",
            ),
        ),
        migrations.AddField(
            model_name='templateversion',
            name='framework_type',
            field=models.CharField(
                choices=[
                    ("RTGO", "RTGO"),
                    ("SPAR", "SPAR"),
                    ("CUSTOM", "Custom"),
                ],
                max_length=10,
                verbose_name="框架类型",
                default="CUSTOM",
            ),
        ),
    ]