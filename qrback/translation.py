from modeltranslation.translator import translator, TranslationOptions

from qrback.models import Entry, FoodGroup, FoodCategory


# python manage.py sync_translation_fields
# python manage.py update_translation_fields


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'detail',)
    required_languages = ('tr',)


class FoodTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('tr',)


translator.register(Entry, ProductTranslationOptions)
translator.register(FoodGroup, FoodTranslationOptions)
translator.register(FoodCategory, FoodTranslationOptions)
