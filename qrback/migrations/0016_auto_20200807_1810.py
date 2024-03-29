# Generated by Django 3.0.8 on 2020-08-07 18:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0015_auto_20200806_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_entry',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account_entry',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='closed_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='first_order_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='last_order_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
