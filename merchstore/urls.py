from django.urls import path

from . import views

app_name = 'merchstore'

urlpatterns = [
    path('items', views.ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('item/add', views.ProductCreateView.as_view(), name='product-create'),
    path('item/<int:pk>/edit', views.product_update_view, name='product-update'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('transactions', views.TransactionListView.as_view(),
         name='transaction-list'),
]
