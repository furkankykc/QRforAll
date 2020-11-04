import os
from shutil import make_archive

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from qrback import service, optimization
from qrback.models import Company, Entry, FoodCategory, Accounting, Category, Account_Entry
from qrforall import settings
from django.db.models import Q
import json

from qrforall import settings


def index(request):
    context = {'companies': Company.objects.filter(hide_on_referances=False).exclude(logo__exact='')}
    return render(request, template_name='test/index.html', context=context)


def optimize_images(request):
    if request.user.is_superuser:
        optimization.optimize_images()
    return redirect('index')


def check_accounting_entry(request, slug, order_id):
    Account_Entry.objects.get(id=order_id).checked()

    return redirect('panel', slug)


def delete_accounting_entry(request, slug, order_id):
    Account_Entry.objects.get(id=order_id).delete()

    return redirect('panel', slug)


def remove_accounting_entry(request, slug, order_id):
    Account_Entry.objects.get(id=order_id).delete_order()

    return redirect('panel', slug)


def check_out_table(request, slug, category_slug, table_id: int):
    company = Company.objects.get(slug=slug)
    category = Category.objects.get(slug=category_slug)
    Accounting.get_table_account(company, table_id, category).withdraw()
    return redirect('panel', slug)


def request_garson(request, slug, category_slug, table_id: int):
    company = Company.objects.get(slug=slug)
    category = Category.objects.get(slug=category_slug)
    Accounting.get_table_account(company, table_id, category).request_garson()
    return redirect('menu-detail', company.prefix, slug, category_slug, table_id)


def garson_is_on_the_way(request, slug, category_slug, table_id: int):
    company = Company.objects.get(slug=slug)
    category = Category.objects.get(slug=category_slug)
    Accounting.get_table_account(company, table_id, category).garson_has_requested()
    return redirect('panel', slug)


@login_required
def panel(request, slug):
    # accounting_all = Accounting.objects.filter(company__slug=slug, is_closed=False)
    # Account_Entry.objects.filter(id_in)
    try:
        _slug = Company.objects.get(owner=request.user).slug
    except Company.DoesNotExist:
        _slug = "-1"
    if not request.user.is_superuser:
        if _slug != slug:
            return redirect('index')

    acc = Accounting.objects.filter(company__slug=slug, is_closed=False)
    acc = acc.annotate(num_participants=Count('order_list')).filter(
        Q(num_participants__gt=0) | Q(requesting_garson=True)).order_by('-last_order_time')
    context = {
        # .filter(order_list__count__gt=0)
        'accounting': acc,
        'company': Company.objects.get(slug=slug)
    }
    return render(request, template_name='digitalMenuPanel.html', context=context)


def test(request, slug):
    company = Company.objects.get(slug__exact=slug)

    return render(request, template_name='menu/digitalMenuNotOrder.html',
                  context={'company': company,
                           'entries': Entry.objects.filter(company=company.id).order_by('category__group',
                                                                                        'category__name')})


def orderDetail(request, *args, **kwargs):
    slug = kwargs['slug']
    table_id = kwargs['table_id']
    category = None
    if 'category_slug' in kwargs:
        category_slug = kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
    company = Company.objects.get(slug=slug)
    accounting = Accounting.get_table_account(company, table_id, category)
    context = {'accounting': accounting}
    return render(request, template_name='digitalAccounting.html', context=context)


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


def menu_no_table(request, slug, category_id, prefix):
    company = Company.objects.get(slug__exact=slug, prefix__exact=prefix)
    return render(request, template_name='digitalMenuItem.html',
                  context={'categories': Entry.objects.filter(company_id=company.id, category=category_id),
                           'company': company, 'category_id': category_id})


def due_date(request):
    if request.user.is_superuser:
        return HttpResponse(
            Company.set_initial_due_date())


# def handler404(request, exception):
#     return render(request, 'errors/404.html', locals())

def menu(request, *args, **kwargs):
    slug = kwargs['slug']
    prefix = kwargs['prefix']
    category_slug = None
    if 'category_slug' in kwargs:
        category_slug = kwargs['category_slug']
    table_id = -1
    category_id = 0
    if 'table_id' in kwargs:
        table_id = kwargs['table_id']
    if 'category_id' in kwargs:
        category_id = kwargs['category_id']

    # company = Company.objects.get(slug__exact=slug)
    company = get_object_or_404(Company, slug__exact=slug, prefix__exact=prefix)

    max_table_count = company.account_type.count_of_max_table
    table_category = None
    if company.account_type.categories.filter(slug=category_slug).exists():
        table_category = Category.objects.get(slug=category_slug)
        category_slug = table_category.slug
    else:
        category_slug = company.account_type.categories.first().slug
    if request.method == "POST":
        count = int(request.POST['count'])
        item_id = int(request.POST['chosen_entry'])
        if table_category is not None:
            account = Accounting.get_table_account(company, table_id, table_category)
        else:
            return HttpResponseNotFound("invalid category")
        entry = Entry.objects.get(id=item_id)

        account.add_entry(entry, count)
        print(entry, '|', count, '| table=', table_id)
        return redirect("category", slug, category_slug, table_id, category_id)
    print('table_category=', category_slug, '| table=', table_id)

    eid = Entry.objects.filter(company__slug=slug).values('category').distinct()
    categories = FoodCategory.objects.filter(id__in=eid)
    # return render(request, template_name='digitalMenuNotOrder.html',
    #               context={'company': company, 'entries': Entry.objects.filter(company=company.id)})

    if company.account_type.has_digital_menu:
        if company.account_type.has_unique_tables:
            if category_id != 0:
                return render(request, template_name='digitalMenuItem.html',
                              context={'categories': Entry.objects.filter(company_id=company.id, category=category_id),
                                       'company': company, 'table_id': table_id, 'category_slug': category_slug,
                                       'category_id': category_id})
            else:
                if table_id == 0 or table_id > max_table_count:
                    return HttpResponseNotFound("Masa sayısı aşıldı")
                elif table_id == -1:
                    company.count()
                    return render(request, template_name='menu/digitalMenuCategory.html',
                                  context={'categories': categories, 'company': company,
                                           'category_id': category_id})
                company.count()
                return render(request, template_name='menu/digitalMenuCategory.html',
                              context={'categories': categories, 'company': company, 'table_id': table_id,
                                       'category_slug': category_slug,
                                       'category_id': category_id})
        else:
            return render(request, template_name='menu/digitalMenuNotOrder.html',
                          context={'company': company,
                                   'entries': Entry.objects.filter(company=company.id).order_by('category__group',
                                                                                                'category__name')})

    else:
        company.count()
        return render(request, template_name='paperMenu.html', context={'company': company})


class MenuDetailView(DetailView):
    model = Company
    template_name = 'paperMenu.html'
    context_object_name = 'company'


def manifest_for_company(request, company):
    company_obj = Company.objects.get(slug=company)
    data_dump = {

        "short_name": f"{company_obj.name}",
        "name": f"{company_obj.name}",
        "start_url": f"/{company_obj.prefix}/{company_obj.slug}/",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "display": "standalone",
        "description": f"{company_obj.slogan}",
        "dir": "ltr",
        "lang": "tr-TR",
        "orientation": "portrait-primary",

        "icons": [{
            "src": f"{settings.HTTP_METHOD}://{settings.SITE_URL}{company_obj.logo_96.url}",
            "type": "image/png",
            "sizes": "192x192"
        }, {
            "src": f"{settings.HTTP_METHOD}://{settings.SITE_URL}{company_obj.logo_512.url}",
            "type": "image/png",
            "sizes": "512x512"
        }]
    }

    data = json.dumps(data_dump)
    return HttpResponse(data, content_type='application/json')
