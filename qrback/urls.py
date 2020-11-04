from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from qrback.admin import customAdminSite
from qrback.views import *

# handler404 = 'qrback.views.handler404'

urlpatterns = [
    path('panel/<slug:slug>/', panel, name='panel'),
    path('login/', customAdminSite.login, name='login'),

    path('order/<slug:slug>/<slug:category_slug>/<int:table_id>/category/<int:category_id>', menu, name='order'),
    path('detail/<slug:slug>/<slug:category_slug>/<int:table_id>', orderDetail, name='order-detail'),
    path('garson/<slug:slug>/<slug:category_slug>/<int:table_id>', request_garson, name='garson'),
    path('send/garson/<slug:slug>/<slug:category_slug>/<int:table_id>', garson_is_on_the_way, name='check_garson'),
    path('checkout/<slug:slug>/<slug:category_slug>/<int:table_id>', check_out_table, name='check-out-table'),

    path('check/<slug:slug>/<int:order_id>/', check_accounting_entry, name='check'),
    path('delete/<slug:slug>/<int:order_id>/', delete_accounting_entry, name='delete'),
    path('remove/<slug:slug>/<int:order_id>/', remove_accounting_entry, name='remove'),
    path('qr/<slug:slug>/', QRDetailView.as_view(), name='generate_qr'),
    path('optimize/', optimize_images, name='optimize_images'),
    path('due_date/', due_date, name='due_date'),
    path('download/<slug:slug>/', download, name='download'),
    path('manifest/<slug:company>/', manifest_for_company, name='manifest'),
    path('test/<slug:slug>/', test, name='test'),
    path('', index, name='index'),
    path('<slug:prefix>/<slug:slug>/', menu, name='menu-detail'),
    path('<slug:prefix>/<slug:slug>/category/<int:category_id>', menu_no_table, name='category'),
    path('<slug:prefix>/<slug:slug>/<slug:category_slug>/<int:table_id>', menu, name='menu-detail'),
    path('<slug:prefix>/<slug:slug>/<slug:category_slug>/<int:table_id>/category/<int:category_id>', menu,
         name='category'),
    path(r'service-worker.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="service-worker.js",
        content_type='application/javascript',
    )), name='service-worker.js'),

]
