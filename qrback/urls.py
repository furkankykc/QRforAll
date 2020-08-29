from django.urls import path

from qrback.admin import customAdminSite
from qrback.views import *

urlpatterns = [
    path('panel/<slug:slug>/', panel, name='panel'),
    path('login/', customAdminSite.login, name='login'),
    path('menu/<slug:slug>/', menu, name='menu-detail'),
    path('menu/<slug:slug>/category/<int:category_id>', menu_no_table, name='category'),
    # path('menu/<slug:slug>/<int:table_id>', menu, name='menu-detail'),
    # path('menu/<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='category'),
    # path('order/<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='order'),
    # path('detail/<slug:slug>/<int:table_id>', orderDetail, name='order-detail'),
    # path('garson/<slug:slug>/<int:table_id>', request_garson, name='garson'),
    # path('send/garson/<slug:slug>/<int:table_id>', garson_is_on_the_way, name='check_garson'),
    # path('checkout/<slug:slug>/<int:table_id>/', check_out_table, name='check-out-table'),

    path('menu/<slug:slug>/<slug:category_slug>/<int:table_id>', menu, name='menu-detail'),
    path('menu/<slug:slug>/<slug:category_slug>/<int:category_id>/<int:table_id>/', menu, name='category'),
    path('order/<slug:slug>/<slug:category_slug>/<int:category_id>/<int:table_id>/', menu, name='order'),
    path('detail/<slug:slug>/<slug:category_slug>/<int:table_id>', orderDetail, name='order-detail'),
    path('garson/<slug:slug>/<slug:category_slug>/<int:table_id>', request_garson, name='garson'),
    path('send/garson/<slug:slug>/<slug:category_slug>/<int:table_id>', garson_is_on_the_way, name='check_garson'),
    path('checkout/<slug:slug>/<slug:category_slug>/<int:table_id>/', check_out_table, name='check-out-table'),

    path('check/<slug:slug>/<int:order_id>/', check_accounting_entry, name='check'),
    path('delete/<slug:slug>/<int:order_id>/', delete_accounting_entry, name='delete'),
    path('remove/<slug:slug>/<int:order_id>/', remove_accounting_entry, name='remove'),
    path('qr/<slug:slug>/', QRDetailView.as_view(), name='generate_qr'),
    path('download/<slug:slug>/', download, name='download'),
    path('test/<slug:slug>/', test, name='test'),
    path('', index, name='index'),
]
