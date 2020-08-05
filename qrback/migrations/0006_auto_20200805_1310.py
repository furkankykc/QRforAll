# Generated by Django 3.0.8 on 2020-08-05 13:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0005_entry_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='facebook',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='instagram',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='company',
            name='pinterest',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='tripadvisor',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='twitter',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='youtube',
            field=models.URLField(blank=True),
        ),
    ]
