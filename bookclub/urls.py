from django.urls import path

from . import views

app_name = 'bookclub'

urlpatterns = [
    path('books', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/add', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/borrow', views.BookBorrowView.as_view(), name='book-borrow'),
    path('book/<int:pk>/edit', views.book_update_view, name='book-update'),
]
