from django import forms
from .models import Event, EventSignup

class EventForm(forms.ModelForm): 
    class Meta: 
        model = Event 
        exclude = ['organizer', 'category']
    
class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']