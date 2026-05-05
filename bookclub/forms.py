from django import forms
from .models import BookReview, Borrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['anon_reviewer', 'title', 'comment']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_to_return']


