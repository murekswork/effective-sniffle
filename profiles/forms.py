from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileCreationForm(ModelForm):

    age = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'orientation', 'location']