from django.urls import include, path
from rest_framework import routers
from qrest import views

router = routers.DefaultRouter()
router.register(r'companys', views.CompanyViewSet)
router.register(r'types', views.TypeViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
