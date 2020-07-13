from django.contrib import admin

from qrback.models import *

admin.site.register(Category)
admin.site.register(AccountType)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # fields = ('slug', 'name', 'account_type', 'categories', 'menu')
    prepopulated_fields = {'slug': ('name',)}

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['slug'].disabled = True
        form.base_fields['slug'].help_text = "This field is not editable"
        return form


