import os

from django.db import models
from django.db.models import Sum, QuerySet, F
from django.db.models.functions import Coalesce
from django.forms import FloatField
from django.utils.text import slugify

from qrback import service
from qrforall import settings


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
    count_of_max_table = models.IntegerField(default=50)
    extra_fee = models.FloatField(default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=20)
    menu = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    slug = models.SlugField(blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)

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


class FoodCategory(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    category = models.ManyToManyField(FoodCategory)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Account_Entry(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    count = models.IntegerField(default=0)


class Accounting(models.Model):
    table = models.IntegerField()
    order_list = models.ManyToManyField(Account_Entry, blank=True)
    first_order_time = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    checked_money = models.FloatField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def add_entry(self, entry: Entry, count: int = 1):
        obj, _ = self.order_list.get_or_create(name=entry.name)
        obj.price = entry.price
        obj.name = entry.name
        obj.count = obj.count + count
        obj.save()

    def withdraw(self, money=0):
        borrowed = 0
        if money != 0:
            borrowed = self.get_borrow() - money
        else:
            self.checked_money = self.get_borrow()
        if borrowed == 0:
            self.is_closed = True

    @property
    def get_borrow(self):
        sum = 0
        if self.order_list.exists():
            sum = list(self.order_list.all().annotate(total_spent=Sum(
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
