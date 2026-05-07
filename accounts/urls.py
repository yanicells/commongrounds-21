from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('<str:username>', views.ProfileUpdateView.as_view(), name='profile_update'),
]
