from django.urls import path

from .views import EventDetailView, EventListView, EventCreateView, EventUpdateView, EventSignupView

app_name = 'localevents'

urlpatterns = [
    path('events', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/add', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:event_pk>/signup', EventSignupView.as_view(), name='event_signup'),
]
