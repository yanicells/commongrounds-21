from django import forms
from .models import Book, BookReview, Borrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['anon_reviewer', 'title', 'comment']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'borrow_date']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'synopsis', 'publication_year', 'available_to_borrow']


