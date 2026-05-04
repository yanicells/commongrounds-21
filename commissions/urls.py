from django.urls import path
from .views import *

from . import views

app_name = 'commissions'

urlpatterns = [
    path('requests', views.RequestListView.as_view(), name='request-list'),
    path('request/<int:pk>', views.RequestDetailView.as_view(),
         name='request-detail'),
]
