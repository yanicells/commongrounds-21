<<<<<<< HEAD
from django.views.generic import DetailView, ListView

from .models import Commission


class RequestListView(ListView):
    model = Commission
    template_name = 'commissions/request_list.html'
    context_object_name = 'commissions'


class RequestDetailView(DetailView):
    model = Commission
    template_name = 'commissions/request_detail.html'
    context_object_name = 'commission'
=======
from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class CommissionListView(ListView):
    model = Commission
    template_name = ''

class CommissionDetailView(DetailView):
    model = Commission
    template_name = ''
>>>>>>> 9693708 (fix: urls and missing model field)
