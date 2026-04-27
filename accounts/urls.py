from django.urls import path
from .views import RegisterView, ProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile_update'),
]
