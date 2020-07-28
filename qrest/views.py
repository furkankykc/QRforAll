from qrback.models import *
from rest_framework import viewsets
from qrest.serializers import CompanySerializer, TypeSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """quickstart
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = AccountType.objects.all()
    serializer_class = TypeSerializer
