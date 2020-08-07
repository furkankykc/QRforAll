from django.urls import path

from qrback.views import MenuDetailView, QRDetailView, download, menu, orderDetail, test, panel, check_accounting_entry, \
    delete_accounting_entry, check_out_table

urlpatterns = [
    path('menu/<slug:slug>/', menu, name='menu-detail'),
    path('menu/<slug:slug>/<int:table_id>', menu, name='menu-detail'),
    path('menu/<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='category'),
    path('order/<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='order'),
    path('panel/<slug:slug>/', panel, name='panel'),
    path('detail/<slug:slug>/<int:table_id>', orderDetail, name='order-detail'),
    path('garson/<slug:slug>/<int:table_id>', menu, name='garson'),
    path('qr/<slug:slug>/', QRDetailView.as_view(), name='generate_qr'),
    path('download/<slug:slug>/', download, name='download'),
    path('test/<slug:slug>/', test, name='test'),
    path('check/<slug:slug>/<int:order_id>/', check_accounting_entry, name='check'),
    path('checkout/<slug:slug>/<int:table_id>/', check_out_table, name='check-out-table'),
    path('delete/<slug:slug>/<int:order_id>/', delete_accounting_entry, name='delete'),
]
