from django.db import models
from django.urls import reverse
from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contributor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField()
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("bookclub:book-detail", args=[str(self.pk)])


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    anon_reviewer = models.CharField(max_length=255, blank=True, null=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()


class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    date_bookmarked = models.DateTimeField(auto_now_add=True)


class Borrow(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    borrower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    date_to_return = models.DateTimeField()
