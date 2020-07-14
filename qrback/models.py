import os

from django.db import models
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