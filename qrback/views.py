from django.shortcuts import render
from django.views.generic import DetailView

from qrback.models import Company


def index(request):
    context = {}
    return render(request, template_name='index.html', context=context)


class MenuDetailView(DetailView):
    model = Company
    template_name = 'menu.html'
    context_object_name = 'company'
