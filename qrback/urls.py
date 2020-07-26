from django.urls import path

from qrback.views import MenuDetailView, QRDetailView, download, menu, orderDetail, test

urlpatterns = [
    path('menu/<slug:slug>/', menu, name='menu-detail'),
    path('menu/<slug:slug>/<int:table_id>', menu, name='menu-detail'),
    path('detail/<slug:slug>/<int:table_id>', orderDetail, name='order-detail'),
    path('garson/<slug:slug>/<int:table_id>', menu, name='garson'),
    path('menu/<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='category'),
    path('order/<slug:slug>/<int:table_id>/<int:category_id>', menu, name='order'),
    path('qr/<slug:slug>/', QRDetailView.as_view(), name='generate_qr'),
    path('download/<slug:slug>/', download, name='download'),
    path('test/<slug:slug>/', test, name='test'),
]
