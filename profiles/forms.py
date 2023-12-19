from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'orientation', 'location', 'age']