from django.urls import path

from . import views

app_name = 'merchstore'

urlpatterns = [
    path('items', views.ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/add', views.ItemCreateView.as_view(), name='item-add'),
    path('item/<int:pk>/edit', views.item_update_view, name='item-update'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('transactions', views.TransactionListView.as_view(),
         name='transaction-list'),
]
