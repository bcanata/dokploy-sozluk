from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear the cached site settings (logo/favicon) to force reload"

    def handle(self, *args, **options):
        cache.delete("default_context__site_settings")
        self.stdout.write(self.style.SUCCESS("Site settings cache cleared successfully!"))
        self.stdout.write("New logo/favicon will be loaded on next page refresh.")
