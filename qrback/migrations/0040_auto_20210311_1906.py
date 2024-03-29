# Generated by Django 3.0.8 on 2021-03-11 16:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0039_auto_20201105_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttype',
            name='has_pdf',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='company',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 11, 16, 6, 53, 974245, tzinfo=utc), verbose_name='Lisans bitiş tarihi'),
        ),
    ]
