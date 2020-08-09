from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import title
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group

from qrback.models import *


# admin.site.register(Entry)
class CustomAdminSite(admin.AdminSite):
    site_title = "Karekod Yazılımı"
    site_header = "Karekod Yazılımı"
    index_title = "Karekod Yazılımı"

    def each_context(self, request):
        context = super().each_context(request)
        if request.user.is_authenticated:
            try:
                comp = Company.objects.get(owner=request.user).slug
            except Company.DoesNotExist:
                comp = ""

            context.update({
                'slug': comp
            })
        return context


customAdminSite = CustomAdminSite()
customAdminSite.register(Category)
customAdminSite.register(AccountType)
customAdminSite.register(User)
customAdminSite.register(Group)


@admin.register(Entry, site=customAdminSite)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'company', 'image')

    # def __init__(self, *args, **kwargs):
    #     super(EntryAdmin, self).__init__(*args, **kwargs)
    #     self.fields['category'].queryset = FoodCategory.objects.filter(owner=)  # or something else
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:  # editing an existing object
            return self.readonly_fields + ('company',)
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                kwargs["queryset"] = FoodCategory.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(EntryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # self.fields['category'].queryset = FoodCategory.objects.filter(owner=request.user)  # or something else
        return qs.filter(company__owner=request.user)


@admin.register(FoodCategory, site=customAdminSite)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','group')
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:  # editing an existing object
            return self.readonly_fields + ('owner',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user
        super(FoodCategoryAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "owner":
                kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(FoodCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(FoodGroup, site=customAdminSite)
class FoodGroupAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:  # editing an existing object
            return self.readonly_fields + ('owner',)
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "owner":
                kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user
        super(FoodGroupAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(FoodGroupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Company, site=customAdminSite)
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

    # change_form_template = "admin/base_site.html"

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            matching_names_except_this.delete()
            obj.name = ""
            obj.save()
            self.message_user(request, "This villain is now unique")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
