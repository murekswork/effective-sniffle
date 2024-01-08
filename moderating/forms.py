from .models import Complain
from django.forms import ModelForm
from django import forms

class ComplainForm(ModelForm):

    class Meta:
        model = Complain
        fields = ['reason', 'description']