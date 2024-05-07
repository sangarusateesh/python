# forms.py
from django.forms import ModelForm
from django import forms
from .models import users as UserProfile

class RegistrationForm(ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'sattttt'}))
    class Meta:
        model = UserProfile
        fields = ['email', 'userPhone', 'user_name']  # Add more fields as needed
