import os
from tempfile import NamedTemporaryFile
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.db.models import Sum, F
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from image_optimizer.fields import OptimizedImageField
from qrback import service
from django.utils import timezone

from io import BytesIO, StringIO
from django.core.files import File
from PIL import Image

from qrback.validators import validate_file_extension


def get_image_path(instance, filename) -> str:
    return os.path.join('photos', str(instance.id), filename)


def get_pdf_path(instance, filename) -> str:
    return os.path.join('pdf', str(instance.company.name), filename)


def image_to_byte_array(image: Image):
    imgByteArr = BytesIO()
    image.save(imgByteArr, format="PNG")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name.title()


class AccountType(models.Model):
    name = models.CharField(max_length=20)
    has_unique_tables = models.BooleanField(default=False)
    has_unique_categories = models.BooleanField(default=False)
    has_digital_menu = models.BooleanField(default=False)
    has_whatsapp_order = models.BooleanField(default=False)
    has_pdf = models.BooleanField(default=False)
    count_of_max_table = models.IntegerField(default=50)
    extra_fee = models.FloatField(default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmalar'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='sahip')
    slug = models.SlugField(blank=True, verbose_name='url')
    prefix = models.SlugField(blank=False, null=False, default='menu', verbose_name='prefix')
    name = models.CharField(max_length=20, verbose_name='İsim')
    slogan = models.CharField(max_length=40, blank=True, null=True)
    menu = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                             help_text=_("Bu kısım resim bazlı menü kullanan kullanıcılarımıza özeldir"))
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, verbose_name='Hesap tipi')
    is_active = models.BooleanField(default=True, verbose_name="Aktiflik Durumu")
    due_date = models.DateTimeField(default=timezone.now() + relativedelta(months=12),
                                    verbose_name='Lisans bitiş tarihi')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    email_regex = RegexValidator(regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                                 message="Email address must be entered in the format: 'example@mail.com'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True, verbose_name='telefon')  # validators should be a list
    phonesecond = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                   null=True, verbose_name='telefon 2')  # validators should be a list
    email = models.CharField(validators=[email_regex], max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True, verbose_name='adres')
    logo = OptimizedImageField(
        upload_to=get_image_path,
        blank=True,
        null=True,
        verbose_name='Logo',
        optimized_image_output_size=(480, 480),
        optimized_image_resize_method='thumbnail')
    logo_96 = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name="192x logo")
    logo_512 = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name="512x logo")
    menu_background = OptimizedImageField(
        upload_to=get_image_path, blank=True, null=True,
        help_text="Bu kısım sadece dijital menü kullanan kullanıcılarımıza özeldir",
        verbose_name='dijital menü banner',
        optimized_image_output_size=(480, 480),
        optimized_image_resize_method='thumbnail')
    not_order_background = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                             help_text="Bu kısım sadece siparişsiz dijital menü kullanan kullanıcılarımıza özeldir",
                                             verbose_name='siparissiz menü arkaplani'
                                             )
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True,
                               help_text='http://api.whatsapp.com/send?phone=+90********** şeklinde girilmelidir')

    counter = models.IntegerField(default=0, verbose_name='Menü görüntülenme sayısı')
    hide_on_referances = models.BooleanField(default=False,
                                             help_text="Referanslarimiz içerisinde gözükmek istemiyorsanız bu kutucuğu işaretleyerek bunu belirtebilirsiniz.",
                                             verbose_name='referanslar listesinden gizle')

    def count(self):
        count = self.counter
        if count is None:
            count = 1
        else:
            count = count + 1
        self.counter = count
        self.save()

    def get_menu_num(self):
        return range(1, self.account_type.count_of_max_table)

    @classmethod
    def set_initial_due_date(cls):
        for comp in cls.objects.all():
            if comp.owner:
                comp.due_date = comp.owner.date_joined + relativedelta(months=12)
                comp.save()

    def renew_payment(self, credit=12):
        pay_today = timezone.now()
        if self.due_date < pay_today:
            self.due_date = pay_today + relativedelta(months=credit)
        else:
            self.due_date += relativedelta(months=credit)

    @property
    def get_company_is_active(self):
        return self.is_active and self.due_date > timezone.now()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        previous_logo = None
        if self.id is not None:
            previous_logo = Company.objects.get(id=self.id).logo

        super(Company, self).save(*args, **kwargs)
        if self.logo and self.logo != previous_logo:
            im = Image.open(self.logo.path)
            im1 = im.resize((192, 192))
            im2 = im.resize((512, 512))

            # Create a file-like object to write thumb data (thumb data previously created
            # using PIL, and stored in variable 'thumb')
            thumb_io1 = BytesIO()
            thumb_io2 = BytesIO()
            im1.save(thumb_io1, format='png')
            im2.save(thumb_io2, format='png')

            thumb_file1 = InMemoryUploadedFile(
                file=thumb_io1,
                field_name=None,
                name=f"{self.logo.name.split('.')[0]}_192.{self.logo.name.split('.')[1]}",
                content_type="PNG",
                size=im1.size,
                charset=None
            )
            thumb_file2 = InMemoryUploadedFile(
                file=thumb_io2,
                field_name=None,
                name=f"{self.logo.name.split('.')[0]}_512.{self.logo.name.split('.')[1]}",
                content_type="PNG",
                size=im2.size,
                charset=None
            )

            self.logo_96.save(thumb_file1.name, thumb_file1, save=False)
            self.logo_512.save(thumb_file2.name, thumb_file2, save=False)

            # tempfile_io1 = BytesIO()
            # tempfile_io2 = BytesIO()
            # im1.save(tempfile_io1, format='JPEG')
            # image_file1 = InMemoryUploadedFile(tempfile_io1, None, 'rotate.jpg', 'image/jpeg', tempfile_io1.len, None)
            # image_file2 = InMemoryUploadedFile(tempfile_io1, None, 'rotate2.jpg', 'image/jpeg', tempfile_io2.len, None)
            #
            # im1.save(f"{self.logo.name.split[0]}_192.{self.logo.name.split('.')[1]}", image_file1)
            # im2.save(f"{self.logo.name.split[0]}_512.{self.logo.name.split('.')[1]}", image_file2)

            super(Company, self).save(*args, **kwargs)

    @property
    def create_qr(self):
        qr_list = [service.create_qr(self)]
        if self.account_type.has_unique_tables:
            for j in self.account_type.categories.all():
                qr_list.extend(
                    [service.create_qr(self, j.slug, i) for i in range(1, self.account_type.count_of_max_table + 1)])
        return qr_list

    def __str__(self):
        return self.name


class FoodGroup(models.Model):
    class Meta:
        verbose_name = 'Menü Grubu'
        verbose_name_plural = 'Menü Grupları'

    name = models.CharField(max_length=20, verbose_name=_('isim'))
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='sahip')

    def __str__(self):
        return self.name


class Document(models.Model):
    class Meta:
        verbose_name = 'Döküman'
        verbose_name_plural = 'Döküman'
        unique_together = ('company', 'slug',)

    name = models.CharField(max_length=100, verbose_name='isim')
    slug = models.SlugField(blank=True)
    document = models.FileField(upload_to=get_pdf_path, blank=True, null=True, verbose_name='dosya',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_doc', verbose_name='sirket')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Document, self).save(*args, **kwargs)

    @property
    def create_qr(self):
        qr_list = service.create_qr_pdf(self)
        return qr_list


class FoodCategory(models.Model):
    class Meta:
        verbose_name = 'Menü Kategorisi'
        verbose_name_plural = 'Menü Kategorileri'

    name = models.CharField(max_length=20, verbose_name=_('isim'))
    image = OptimizedImageField(
        upload_to=get_image_path,
        blank=True,
        null=True,
        verbose_name='kapak fotoğrafı',
        optimized_image_output_size=(480, 480),
        optimized_image_resize_method='thumbnail'  # 'thumbnail', 'cover' or None
    )
    is_abstract = models.BooleanField(default=False, verbose_name='soyut',
                                      help_text='Aktifleştirildiğinde bu kategoride bulunan ürünlerin fiyatları müşterilere gösterilmez.(sadece dijital siparişli menü içindir)')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='sahip')
    group = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='grup')

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image


class Entry(models.Model):
    class Meta:
        verbose_name = 'Menü Ürünü'
        verbose_name_plural = 'Menü Ürünleri'

    name = models.CharField(max_length=30, verbose_name=_('isim'))
    detail = models.CharField(max_length=100, verbose_name=_('ürün detayı'), blank=True)
    price = models.FloatField(verbose_name='fiyat')
    image = OptimizedImageField(
        upload_to=get_image_path,
        blank=True,
        null=True,
        verbose_name='kapak fotoğrafı',
        optimized_image_output_size=(480, 480),
        optimized_image_resize_method='thumbnail'  # 'thumbnail', 'cover' or None
    )
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, verbose_name='Kategori')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_entry', verbose_name='sirket')

    @property
    def get_image(self):
        return self.image or self.category.image

    def __str__(self):
        return self.name


class Account_Entry(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    is_checked = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)
    is_delivered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def delete_order(self):
        self.is_deleted = True
        self.save()

    def checked(self):
        if self.is_checked:
            self.is_delivered = True
        else:
            self.is_checked = True
        self.save()


class Accounting(models.Model):
    table = models.IntegerField()
    order_list = models.ManyToManyField(Account_Entry, blank=True)
    first_order_time = models.DateTimeField(default=timezone.now)
    last_order_time = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    checked_money = models.FloatField(default=0)
    requesting_garson = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def request_garson(self):
        self.requesting_garson = True
        self.save()

    def garson_has_requested(self):
        self.requesting_garson = False
        self.save()

    def add_entry(self, entry: Entry, count: int = 1):
        obj, _ = self.order_list.get_or_create(name=entry.name, is_checked=False)

        obj.price = entry.price
        obj.name = entry.name
        obj.count = obj.count + count
        obj.save()
        self.last_order_time = timezone.now()
        self.save()

    def withdraw(self, money=0):
        borrowed = 0
        if money != 0:
            borrowed = self.get_borrow - money
        else:
            self.checked_money = self.get_borrow
            self.save()
        if borrowed == 0:
            self.is_closed = True
            self.closed_at = timezone.now()
        else:
            self.checked_money = money
        self.save()

    @property
    def get_borrow(self):
        sum = 0
        if self.order_list.exists():
            order_list = self.order_list.filter(is_deleted=False, is_checked=True)
            if order_list.count() > 0:
                sum = list(order_list.annotate(total_spent=Sum(
                    F('price') *
                    F('count'),
                    output_field=models.FloatField()
                )).aggregate(Sum('total_spent')).values())[0] - self.checked_money
        return sum

    @classmethod
    def get_table_account(cls, company, table_id, category):
        if category is not None:
            ses_table = cls.objects.filter(company=company, is_closed=False, table=table_id,
                                           category=category).last()
        else:
            ses_table = cls.objects.filter(company=company, is_closed=False, table=table_id).last()

        if ses_table == None:
            ses_table = cls()
            ses_table.table = table_id
            ses_table.company = company
            if category is None:
                category = company.account_type.categories.first()
            ses_table.category = category
            ses_table.save()
        return ses_table

    def __str__(self):
        return 'Accounting table {}'.format(self.table)
