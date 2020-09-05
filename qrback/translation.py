from modeltranslation.translator import translator, TranslationOptions

from qrback.models import Entry, FoodGroup, FoodCategory


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'detail')
    required_languages = ('en', 'tr')


class FoodTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'tr')


translator.register(Entry, ProductTranslationOptions)
translator.register(FoodGroup, FoodTranslationOptions)
translator.register(FoodCategory, FoodTranslationOptions)
