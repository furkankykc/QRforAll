# Generated by Django 3.0.8 on 2020-08-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrback', '0014_auto_20200806_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_entry',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='first_order_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='last_order_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
