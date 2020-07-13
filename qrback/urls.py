from django.urls import path

from qrback.views import MenuDetailView

urlpatterns = [
    path('<slug:slug>/', MenuDetailView.as_view(), name='menu-detail'),
]