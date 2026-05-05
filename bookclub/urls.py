from django.urls import path

from . import views

app_name = 'bookclub'

urlpatterns = [
    path('books', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/review', views.BookReviewCreateView.as_view(), name='book-review-create'),
    path('book/<int:pk>/bookmark', views.BookmarkCreateView.as_view(), name='book-bookmark'),
    path('book/<int:pk>/borrow', views.BookBorrowView.as_view(), name='book-borrow'),
    path('book/<int:pk>/edit', views.BookUpdateView.as_view(), name='book-edit'),
]
