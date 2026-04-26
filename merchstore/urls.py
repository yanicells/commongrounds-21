from django.urls import path

from . import views

app_name = 'merchstore'

urlpatterns = [
    path('items', views.ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
]
