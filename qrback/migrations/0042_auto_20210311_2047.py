# Generated by Django 3.0.8 on 2021-03-11 17:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import qrback.models


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0041_auto_20210311_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 11, 17, 47, 37, 95309, tzinfo=utc), verbose_name='Lisans bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=qrback.models.get_pdf_path),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('company', 'name')},
        ),
        migrations.RemoveField(
            model_name='document',
            name='owner',
        ),
    ]
