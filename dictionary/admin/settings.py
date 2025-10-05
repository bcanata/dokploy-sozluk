from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from dictionary.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for site-wide settings."""

    fieldsets = (
        (
            _("General"),
            {
                "fields": ("tagline",),
                "description": _("General site settings."),
            },
        ),
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
        (
            _("Content Display"),
            {
                "fields": ("entries_per_page", "topics_per_page"),
                "description": _("Pagination settings for guest users."),
            },
        ),
        (
            _("User Registration"),
            {
                "fields": ("disable_novice_queue",),
                "description": _("Control how new users are registered."),
            },
        ),
        (
            _("Voting Limits"),
            {
                "fields": ("daily_vote_limit", "daily_vote_limit_per_user"),
                "description": _("Rate limits for user voting."),
            },
        ),
        (
            _("Upload Limits"),
            {
                "fields": ("max_upload_size", "daily_image_upload_limit"),
                "description": _("File upload restrictions."),
            },
        ),
        (
            _("Rate Limiting"),
            {
                "fields": ("author_entry_interval", "novice_entry_interval"),
                "description": _("Minimum time between entry submissions."),
            },
        ),
    )

    def has_add_permission(self, request):
        """Prevent adding multiple instances (singleton pattern)."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False

    def save_model(self, request, obj, form, change):
        """Save the model and show a message about cache."""
        super().save_model(request, obj, form, change)
        messages.success(
            request,
            _("Site settings saved successfully! Cache cleared automatically. "
              "New logo/favicon will appear on next page refresh.")
        )
