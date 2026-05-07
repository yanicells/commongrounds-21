from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.mixins import RoleRequiredMixin
from .models import Event, EventSignup
from .forms import EventForm, EventSignupForm


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context["created_events"] = Event.objects.filter(
                organizer=self.request.user.profile)
            context["signed_up_events"] = Event.objects.filter(
                signups__user_registrant=self.request.user.profile)
            context["all_events"] = Event.objects.exclude(organizer=self.request.user.profile).exclude(
                signups__user_registrant=self.request.user.profile)
        else:
            context["all_events"] = Event.objects.all()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventSignupForm()
        event = self.get_object()
        user_profile = None
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            user_profile = self.request.user.profile
        context['is_organizer'] = bool(
            user_profile and event.organizer.filter(pk=user_profile.pk).exists())
        context['has_signed_up'] = bool(user_profile and EventSignup.objects.filter(
            event=event, user_registrant=user_profile).exists())
        context['is_full'] = bool(
            event.event_capacity is not None and event.signups.count() >= event.event_capacity)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return redirect('localevents:event_signup', event_pk=self.object.pk)

        profile = request.user.profile
        if self.object.organizer.filter(pk=profile.pk).exists():
            return redirect(self.object.get_absolute_url())

        if self.object.event_capacity and self.object.signups.count() >= self.object.event_capacity:
            return redirect(self.object.get_absolute_url())

        if EventSignup.objects.filter(event=self.object, user_registrant=profile).exists():
            return redirect(self.object.get_absolute_url())

        form = EventSignupForm(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.event = self.object
            signup.user_registrant = profile
            signup.save()
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class EventCreateView(RoleRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_create_form.html'
    required_role = 'Event Organizer'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        event.organizer.add(self.request.user.profile)
        return redirect(event.get_absolute_url())


class EventUpdateView(RoleRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_update_form.html'
    required_role = 'Event Organizer'

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.event_capacity is not None and event.signups.count() >= event.event_capacity:
            event.status = 'full'
        else:
            event.status = 'available'
        event.save()
        return redirect(event.get_absolute_url())


class BaseSignupView(CreateView):
    model = EventSignup
    form_class = EventSignupForm
    template_name = 'localevents/event_signup_form.html'

    def get_event(self):
        return get_object_or_404(Event, pk=self.kwargs['event_pk'])

    def post(self, request, *args, **kwargs):
        self.event = self.get_event()
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            if not self.check_capacity(self.event):
                return redirect(self.event.get_absolute_url())
            form = self.get_form()
            if form.is_valid():
                form.instance.event = self.event
                form.save()
                return redirect(self.get_redirect_url(self.event))
            else:
                return self.form_invalid(form)

        # Authenticated signup
        user_profile = request.user.profile
        if not self.check_capacity(self.event) or not self.check_ownership(self.event, user_profile):
            return redirect(self.event.get_absolute_url())
        if EventSignup.objects.filter(event=self.event, user_registrant=user_profile).exists():
            return redirect(self.event.get_absolute_url())

        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        self.form = form
        self.create_signup(self.event, user_profile)
        return redirect(self.get_redirect_url(self.event))

    def check_capacity(self, event):
        return event.event_capacity is None or event.signups.count() < event.event_capacity

    def check_ownership(self, event, user):
        return not event.organizer.filter(pk=user.pk).exists()

    def create_signup(self, event, user):
        signup = self.form.save(commit=False)
        signup.event = event
        signup.user_registrant = user
        signup.save()
        return signup

    def get_redirect_url(self, event):
        return event.get_absolute_url()


class EventSignupView(BaseSignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        return context

    def get_redirect_url(self, event):
        # Demonstrating override: redirect to event list instead of event detail
        return reverse('localevents:event_list')
