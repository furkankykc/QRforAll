from django.urls import path

from qrback.views import MenuDetailView, QRDetailView, download, menu

urlpatterns = [
    path('<slug:slug>/', menu, name='menu-detail'),
    path('<slug:slug>/<int:table_id>', menu, name='menu-detail'),
    path('<slug:slug>/<int:category_id>/<int:table_id>/', menu, name='category'),
    path('qr/<slug:slug>/', QRDetailView.as_view(), name='generate_qr'),
    path('download/<slug:slug>/', download, name='download'),
]
