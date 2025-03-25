from django.core.management.base import BaseCommand
from apps.templates.sre_templates import create_sre_templates

class Command(BaseCommand):
    help = 'Creates SRE-related prompt templates'

    def handle(self, *args, **options):
        create_sre_templates()
        self.stdout.write(self.style.SUCCESS('Successfully created SRE templates'))