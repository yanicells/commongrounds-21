from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView

app_name = 'grounds'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/add/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
]
