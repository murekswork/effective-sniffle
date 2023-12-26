from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileCreationForm(ModelForm):

    profile_picture = forms.ImageField(required=True)
    location = forms.Widget(attrs={'value': '{{ location }}'})
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'orientation', 'location', 'age', 'profile_picture']