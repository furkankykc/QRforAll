# Generated by Django 3.0.8 on 2020-08-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0007_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttype',
            name='has_digital_menu',
            field=models.BooleanField(default=False),
        ),
    ]
