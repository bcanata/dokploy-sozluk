from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_add_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='entries_per_page',
            field=models.PositiveIntegerField(default=10, help_text='Number of entries shown per page for guest users', verbose_name='Entries per page (guests)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='topics_per_page',
            field=models.PositiveIntegerField(default=50, help_text='Number of topics shown per page for guest users', verbose_name='Topics per page (guests)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='disable_novice_queue',
            field=models.BooleanField(default=False, help_text='When enabled, new users become authors immediately without approval', verbose_name='Disable novice queue'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='daily_vote_limit',
            field=models.PositiveIntegerField(default=240, help_text='Maximum number of votes a user can cast in 24 hours', verbose_name='Daily vote limit'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='daily_vote_limit_per_user',
            field=models.PositiveIntegerField(default=24, help_text="Maximum votes a user can cast on one author's entries in 24 hours", verbose_name='Daily vote limit per author'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='max_upload_size',
            field=models.PositiveIntegerField(default=2621440, help_text='Maximum file upload size in bytes (1MB = 1048576 bytes)', verbose_name='Max upload size (bytes)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='daily_image_upload_limit',
            field=models.PositiveIntegerField(default=25, help_text='Maximum images a user can upload in 24 hours', verbose_name='Daily image upload limit'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='author_entry_interval',
            field=models.PositiveIntegerField(default=0, help_text='Minimum seconds between entries for authors (0 = no limit)', verbose_name='Entry interval for authors (seconds)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='novice_entry_interval',
            field=models.PositiveIntegerField(default=0, help_text='Minimum seconds between entries for novices (0 = no limit)', verbose_name='Entry interval for novices (seconds)'),
        ),
    ]
