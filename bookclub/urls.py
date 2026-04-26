from django.urls import path

from . import views

app_name = 'bookclub'

urlpatterns = [
    path('books', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
