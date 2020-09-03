# Generated by Django 3.0.8 on 2020-08-29 11:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import qrback.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qrback', '0028_company_hide_on_referances'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Firma', 'verbose_name_plural': 'Firmalar'},
        ),
        migrations.AddField(
            model_name='accounting',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='qrback.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qrback.AccountType', verbose_name='Hesap tipi'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='adres'),
        ),
        migrations.AlterField(
            model_name='company',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='Menü görüntülenme sayısı'),
        ),
        migrations.AlterField(
            model_name='company',
            name='hide_on_referances',
            field=models.BooleanField(default=False, help_text='Referanslarimiz içerisinde gözükmek istemiyorsanız bu kutucuğu işaretleyerek bunu belirtebilirsiniz.', verbose_name='referanslar listesinden gizle'),
        ),
        migrations.AlterField(
            model_name='company',
            name='menu_background',
            field=models.ImageField(blank=True, help_text='Bu kısım sadece dijital menü kullanan kullanıcılarımıza özeldir', null=True, upload_to=qrback.models.get_image_path, verbose_name='dijital menü banner'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=20, verbose_name='İsim'),
        ),
        migrations.AlterField(
            model_name='company',
            name='not_order_background',
            field=models.ImageField(blank=True, help_text='Bu kısım sadece siparişsiz dijital menü kullanan kullanıcılarımıza özeldir', null=True, upload_to=qrback.models.get_image_path, verbose_name='siparissiz menü arkaplani'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='sahip'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='telefon'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phonesecond',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='telefon 2'),
        ),
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='company',
            name='whatsapp',
            field=models.URLField(blank=True, help_text='http://api.whatsapp.com/send?phone=+90********** şeklinde girilmelidir'),
        ),
    ]