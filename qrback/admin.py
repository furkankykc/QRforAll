from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import title
from django.urls import reverse
from django.utils.safestring import mark_safe

from qrback.models import *

admin.site.register(Category)
admin.site.register(AccountType)
admin.site.register(FoodCategory)
admin.site.register(Entry)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # fields = ('slug', 'name', 'account_type', 'categories', 'menu')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'account_type', 'generate_qr')

    # def menuPreview(self, obj):
    #     return mark_safe(
    #         '<images alt="{}"with=50 height=50 src={}/>'.format(obj.name,
    #                                                             os.path.join(settings.MEDIA_URL, obj.logo.url))
    #     )

    def generate_qr(self, obj):
        return mark_safe(
            '<a class="button" title="Generate QR codes" name="index" href="{}">Generate QR</a>'.format(
                'http://127.0.0.1:8000' + reverse('generate_qr', args=([obj.slug]))))

    title.short_description = 'Action'
    title.allow_tags = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['slug'].disabled = True
        form.base_fields['slug'].help_text = "This field is not editable"
        return form

    change_form_template = "admin/change_form.html"

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            matching_names_except_this.delete()
            obj.name = ""
            obj.save()
            self.message_user(request, "This villain is now unique")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
