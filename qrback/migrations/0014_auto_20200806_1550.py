# Generated by Django 3.0.8 on 2020-08-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0013_account_entry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounting',
            name='last_order_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='account_entry',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
