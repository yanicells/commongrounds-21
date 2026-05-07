from django import forms
from .models import Book, BookReview, Borrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'borrow_date']
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'})
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year']

