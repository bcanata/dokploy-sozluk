from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dictionary.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for site-wide settings."""

    fieldsets = (
        (
            _("Logo (Light Theme)"),
            {
                "fields": ("logo_big", "logo_small"),
                "description": _("Upload custom logos for light theme. Leave empty to use default."),
            },
        ),
        (
            _("Logo (Dark Theme)"),
            {
                "fields": ("logo_big_dark", "logo_small_dark"),
                "description": _("Upload custom logos for dark theme. Leave empty to use default."),
            },
        ),
        (
            _("Favicon"),
            {
                "fields": ("favicon",),
                "description": _("Upload custom favicon. Leave empty to use default."),
            },
        ),
    )

    def has_add_permission(self, request):
        """Prevent adding multiple instances (singleton pattern)."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False
