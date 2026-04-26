from django.views.generic import DetailView, ListView

from .models import Product


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'
    context_object_name = 'products'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'
    context_object_name = 'product'
