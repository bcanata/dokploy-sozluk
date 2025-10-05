from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_add_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='tagline',
            field=models.CharField(blank=True, default='özgür bilgi kaynağı', help_text='Tagline displayed in page title (e.g., \'özgür bilgi kaynağı\')', max_length=100, verbose_name='Site Tagline'),
        ),
    ]
