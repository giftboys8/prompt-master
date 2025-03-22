from django.db import migrations

def set_default_visibility(apps, schema_editor):
    Template = apps.get_model('templates', 'Template')
    Template.objects.filter(visibility__isnull=True).update(visibility='PRIVATE')

class Migration(migrations.Migration):
    dependencies = [
        ('templates', '0004_template_visibility'),
    ]

    operations = [
        migrations.RunPython(set_default_visibility),
    ]