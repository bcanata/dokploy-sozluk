from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0006_add_site_settings_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='first_generation_date',
            field=models.DateField(default='2019-08-13', help_text='Date of the first user registration (used for generation calculation)', verbose_name='First generation date'),
        ),
    ]
