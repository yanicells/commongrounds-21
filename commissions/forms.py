from django import forms
from .models import *


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["title",
                  "description",
                  "commission_type",
                  "people_required",
                  "status"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["role",
                  "manpower_required",
                  "status"]
