from django.utils.timezone import now

from qrback.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['name','image']


class EntrySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Entry
        fields = ['name', 'price', 'image', 'category']


class CompanySerializer(serializers.ModelSerializer):
    comp_entry = EntrySerializer(many=True)

    class Meta:
        model = Company
        fields = ['name', 'menu', 'account_type', 'comp_entry']
        # fields = '__all__'


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountType
        fields = ['name', 'has_unique_tables', 'count_of_max_table']
