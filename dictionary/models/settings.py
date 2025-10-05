from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Singleton model for site-wide settings like logo and favicon."""

    # Logo files
    logo_big = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name=_("Logo (Big)"),
        help_text=_("Main logo displayed in header (recommended: 120x40px SVG or PNG)"),
    )
    logo_small = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name=_("Logo (Small)"),
        help_text=_("Small logo for mobile view (recommended: 40x40px SVG or PNG)"),
    )
    logo_big_dark = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name=_("Logo (Big - Dark Theme)"),
        help_text=_("Main logo for dark theme (recommended: 120x40px SVG or PNG)"),
    )
    logo_small_dark = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name=_("Logo (Small - Dark Theme)"),
        help_text=_("Small logo for dark theme mobile view (recommended: 40x40px SVG or PNG)"),
    )

    # Favicon
    favicon = models.FileField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name=_("Favicon"),
        help_text=_("Site favicon (recommended: .ico, .png, or .svg file)"),
    )

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists (singleton pattern)."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of the singleton instance."""
        pass

    @classmethod
    def load(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
