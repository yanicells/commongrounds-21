import profile

from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import role_required
from accounts.mixins import RoleRequiredMixin
from .models import Book, Bookmark, Borrow
from .forms import BookForm, BookReviewForm, BorrowForm
from django.utils import timezone



class BookListView(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile

            context['contributed_books'] = Book.objects.filter(contributor=profile)
            context['bookmarked_books'] = Book.objects.filter(bookmark__profile=profile)
            context['reviewed_books'] = Book.objects.filter(bookreview__user_reviewer=profile)
            context['borrowed_books'] = Borrow.objects.filter(borrower=profile).distinct()
            context['all_books'] = Book.objects.exclude(
                contributor=profile
                ).exclude(
                bookmark__profile=profile
                ).exclude(
                bookreview__user_reviewer=profile
                )
        else:
            context['borrowed_books'] = Borrow.objects.none()
            context['contributed_books'] = Book.objects.none()
            context['bookmarked_books'] = Book.objects.none()
            context['reviewed_books'] = Book.objects.none()
            context['all_books'] = Book.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookclub/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        book = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = BookReviewForm()
        context['is_bookmarked'] = False
        context['bookmarks_count'] = book.bookmark_set.count()
        context['reviews'] = book.bookreview_set.all()
        context['can_edit'] =(
            self.request.user.is_authenticated and
            hasattr(self.request.user, 'profile') and
            book.contributor == self.request.user.profile
        )
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['is_bookmarked'] = Bookmark.objects.filter(profile=self.request.user.profile,
            book=book
        ).exists()


        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'bookmark' in request.POST:
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            profile = request.user.profile
            bookmark_qs = Bookmark.objects.filter(profile=profile, book=self.object)
            if bookmark_qs.exists():
                bookmark_qs.delete()
            else:
                Bookmark.objects.create(profile=profile, book=self.object)
            return redirect(self.object.get_absolute_url())

        form = BookReviewForm(request.POST)
        if form.is_valid():
            book_review = form.save(commit=False)
            book_review.book = self.object
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                book_review.user_reviewer = request.user.profile
                book_review.anon_reviewer = None
            else:
                book_review.user_reviewer = None
                book_review.anon_reviewer = "Anonymous"
            book_review.save()
            return redirect(self.object.get_absolute_url())

        return self.get(request, *args, **kwargs)


class BookCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'
    required_role = 'Book Contributor'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.contributor = self.request.user.profile
        book.save()
        return redirect(book.get_absolute_url())

@role_required('Book Contributor')
def book_update_view(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            updated_book = form.save(commit=False)
            updated_book.contributor = book.contributor
            updated_book.save()
            return redirect(updated_book.get_absolute_url())
    else:
        form = BookForm(instance=book)

    return render(request, 'bookclub/book_form.html', {'form': form, 'book': book})


class BookBorrowView(CreateView):
    model = Book
    form_class = BorrowForm
    template_name = 'bookclub/book_borrow_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            initial['name'] = self.request.user.profile.display_name
        return initial

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        
        borrow_obj = form.save(commit=False)
        borrow_obj.book = book
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            borrow_obj.borrower = self.request.user.profile
            borrow_obj.name = self.request.user.profile.display_name
        else:
            borrow_obj.borrower = None

        borrow_obj.date_to_return = borrow_obj.borrow_date + timezone.timedelta(days=14)
        borrow_obj.save()
        return redirect(book.get_absolute_url())












