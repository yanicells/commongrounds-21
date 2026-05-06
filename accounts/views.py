from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import Profile

from merchstore.models import Product
from localevents.models import Event
from bookclub.models import Book
from diyprojects.models import Project
from commissions.models import Commission


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.success_url)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'registration/profile_update.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user__username=self.kwargs['username'])

    def get_success_url(self):
        return reverse_lazy('home')


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'registration/dashboard.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['events'] = Event.objects.filter(organizer=profile)
        context['books'] = Book.objects.filter(contributor=profile)
        context['projects'] = Project.objects.filter(creator=profile)
        context['commissions'] = Commission.objects.filter(maker=profile)
        return context

