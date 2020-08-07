import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum, QuerySet, F
from django.db.models.functions import Coalesce
from django.forms import FloatField
from django.utils.text import slugify

from qrback import service
from qrforall import settings
from django.utils import timezone


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name.title()


class AccountType(models.Model):
    name = models.CharField(max_length=20)
    has_unique_tables = models.BooleanField(default=False)
    has_unique_categories = models.BooleanField(default=False)
    has_digital_menu = models.BooleanField(default=False)
    count_of_max_table = models.IntegerField(default=50)
    extra_fee = models.FloatField(default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=20)
    menu = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    slug = models.SlugField(blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    email_regex = RegexValidator(regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                                 message="Email address must be entered in the format: 'example@mail.com'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    email = models.CharField(validators=[email_regex], max_length=50, blank=True)

    def get_menu_num(self):
        return range(1, self.account_type.count_of_max_table)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    @property
    def create_qr(self):
        if self.account_type.has_unique_tables:
            return [service.create_qr(self, i) for i in range(1, self.account_type.count_of_max_table + 1)]
        return [service.create_qr(self)]

    def __str__(self):
        return self.name


class FoodGroup(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image


class Entry(models.Model):
    class Meta:
        verbose_name = 'My Food'
        verbose_name_plural = 'My Foods'

    name = models.CharField(max_length=30)
    detail = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_entry')

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
        self.is_deleted=True
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
    closed_at = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    checked_money = models.FloatField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

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
            borrowed = self.get_borrow() - money
        else:
            self.checked_money = self.get_borrow
            self.save()
        if borrowed == 0:
            self.is_closed = True
            self.closed_at = timezone.now()
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
    def get_table_account(cls, company, table_id):
        ses_table = cls.objects.filter(company=company, is_closed=False, table=table_id).last()
        if ses_table == None:
            ses_table = cls()
            ses_table.table = table_id
            ses_table.company = company
            ses_table.save()
        return ses_table

    def __str__(self):
        return 'Accounting table {}'.format(self.table)
