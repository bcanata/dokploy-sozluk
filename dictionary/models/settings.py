from django.core.cache import cache
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

    # Site tagline
    tagline = models.CharField(
        max_length=100,
        blank=True,
        default="özgür bilgi kaynağı",
        verbose_name=_("Site Tagline"),
        help_text=_("Tagline displayed in page title (e.g., 'özgür bilgi kaynağı')"),
    )

    # Content settings
    entries_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Entries per page (guests)"),
        help_text=_("Number of entries shown per page for guest users"),
    )
    topics_per_page = models.PositiveIntegerField(
        default=50,
        verbose_name=_("Topics per page (guests)"),
        help_text=_("Number of topics shown per page for guest users"),
    )

    # Registration settings
    disable_novice_queue = models.BooleanField(
        default=False,
        verbose_name=_("Disable novice queue"),
        help_text=_("When enabled, new users become authors immediately without approval"),
    )

    # Voting limits
    daily_vote_limit = models.PositiveIntegerField(
        default=240,
        verbose_name=_("Daily vote limit"),
        help_text=_("Maximum number of votes a user can cast in 24 hours"),
    )
    daily_vote_limit_per_user = models.PositiveIntegerField(
        default=24,
        verbose_name=_("Daily vote limit per author"),
        help_text=_("Maximum votes a user can cast on one author's entries in 24 hours"),
    )

    # Upload limits
    max_upload_size = models.PositiveIntegerField(
        default=2621440,  # 2.5MB
        verbose_name=_("Max upload size (bytes)"),
        help_text=_("Maximum file upload size in bytes (1MB = 1048576 bytes)"),
    )
    daily_image_upload_limit = models.PositiveIntegerField(
        default=25,
        verbose_name=_("Daily image upload limit"),
        help_text=_("Maximum images a user can upload in 24 hours"),
    )

    # Rate limiting
    author_entry_interval = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Entry interval for authors (seconds)"),
        help_text=_("Minimum seconds between entries for authors (0 = no limit)"),
    )
    novice_entry_interval = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Entry interval for novices (seconds)"),
        help_text=_("Minimum seconds between entries for novices (0 = no limit)"),
    )

    # Generations
    first_generation_date = models.DateField(
        default="2019-08-13",
        verbose_name=_("First generation date"),
        help_text=_("Date of the first user registration (used for generation calculation)"),
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
        # Clear the cached site_settings context processor
        cache.delete("default_context__site_settings")

    def delete(self, *args, **kwargs):
        """Prevent deletion of the singleton instance."""
        pass

    @classmethod
    def load(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
