from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'phone', 'section',
                  'role', 'password1', 'password2')
