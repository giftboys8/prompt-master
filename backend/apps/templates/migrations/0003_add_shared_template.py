from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('templates', '0002_template_target_role_templateversion_target_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_edit', models.BooleanField(default=False, verbose_name='可编辑')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='templates.template', verbose_name='模板')),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with_me', to='auth.user', verbose_name='被分享用户')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_templates', to='auth.user', verbose_name='创建者')),
            ],
            options={
                'verbose_name': '共享模板',
                'verbose_name_plural': '共享模板',
                'unique_together': (('template', 'shared_with'),),
            },
        ),
    ]