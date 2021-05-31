from django import forms
from .models import Quarter_service


class QuarterForm(forms.ModelForm):
    class Meta:
        model = Quarter_service
        fields = ('name', 'phone', "email", "location", "notes", )
