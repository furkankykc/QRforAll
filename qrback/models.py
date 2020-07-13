import os

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from qrforall import settings


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class AccountType(models.Model):
    name = models.CharField(max_length=20)
    has_unique_tables = models.BooleanField(default=False)
    has_unique_categories = models.BooleanField(default=False)
    count_of_max_table = models.IntegerField(default=50)
    extra_fee = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name.title()


class Company(models.Model):
    name = models.CharField(max_length=20)
    menu = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    slug = models.SlugField(blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
