from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_sitesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Profile photo'),
        ),
    ]
