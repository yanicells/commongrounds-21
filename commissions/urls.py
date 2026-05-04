from django.urls import path
from .views import *

from . import views

app_name = 'commissions'

urlpatterns = [
    path('requests', views.CommissionListView.as_view(), name='commission-list'),
    path('request/<int:pk>', views.CommissionDetailView.as_view(),
         name='request-detail'),
]
