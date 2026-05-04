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
