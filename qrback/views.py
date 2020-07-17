import os
from shutil import make_archive

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from qrback import service
from qrback.models import Company, Entry, FoodCategory, Accounting
from qrforall import settings


def index(request):
    context = {}
    return render(request, template_name='index.html', context=context)


def orderDetail(request, *args, **kwargs):
    slug = kwargs['slug']
    table_id = kwargs['table_id']
    company = Company.objects.get(slug=slug)
    accounting = Accounting.get_table_account(company, table_id)
    context = {'accounting': accounting}
    return render(request, template_name='digitalchooser.html', context=context)


def download(request, *args, **kwargs):
    slug = kwargs['slug']
    zippath = os.path.join(settings.MEDIA_ROOT, 'photos')
    make_archive(os.path.join(zippath, slug),
                 'zip',
                 zippath,
                 slug)
    zf = os.path.join(zippath, slug) + '.zip'
    zip_file = open(zf, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % '{}.zip'.format(slug)
    return response


class QRDetailView(DetailView):
    model = Company
    template_name = 'qr.html'
    context_object_name = 'company'


def menu(request, *args, **kwargs):
    slug = kwargs['slug']
    table_id = 0
    category_id = 0
    if 'table_id' in kwargs:
        table_id = kwargs['table_id']
    if 'category_id' in kwargs:
        category_id = kwargs['category_id']
    company = Company.objects.get(slug__exact=slug)
    if request.method == "POST":
        count = int(request.POST['count'])

        account = Accounting.get_table_account(company, table_id)
        entry = Entry.objects.get(id=category_id)

        account.add_entry(entry, count)
    categories = FoodCategory.objects.all()

    if company.account_type.has_unique_tables:
        if category_id != 0:
            return render(request, template_name='digitalmenu.html',
                          context={'categories': Entry.objects.filter(company_id=company.id, category=category_id),
                                   'company': company, 'table_id': table_id, 'category_id': category_id})
        else:
            return render(request, template_name='digitalmenu.html',
                          context={'categories': categories, 'company': company, 'table_id': table_id,
                                   'category_id': category_id})
    else:
        return render(request, template_name='menu.html', context={'company': company})


class MenuDetailView(DetailView):
    model = Company
    template_name = 'menu.html'
    context_object_name = 'company'
