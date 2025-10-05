# Generated manually for SiteSettings model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_author_unique_author_lower_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_big', models.ImageField(blank=True, help_text='Main logo displayed in header (recommended: 120x40px SVG or PNG)', null=True, upload_to='site/', verbose_name='Logo (Big)')),
                ('logo_small', models.ImageField(blank=True, help_text='Small logo for mobile view (recommended: 40x40px SVG or PNG)', null=True, upload_to='site/', verbose_name='Logo (Small)')),
                ('logo_big_dark', models.ImageField(blank=True, help_text='Main logo for dark theme (recommended: 120x40px SVG or PNG)', null=True, upload_to='site/', verbose_name='Logo (Big - Dark Theme)')),
                ('logo_small_dark', models.ImageField(blank=True, help_text='Small logo for dark theme mobile view (recommended: 40x40px SVG or PNG)', null=True, upload_to='site/', verbose_name='Logo (Small - Dark Theme)')),
                ('favicon', models.FileField(blank=True, help_text='Site favicon (recommended: .ico, .png, or .svg file)', null=True, upload_to='site/', verbose_name='Favicon')),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]
