from django.forms import ModelForm
from .models import Profile, UploadedProfilePictures
from django import forms



class ProfileCreationForm(ModelForm):


    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'orientation', 'location', 'age', 'relation_formats', 'interests']
        widgets = {
            'age': forms.DateInput(attrs={'type': 'date'}),
        }


class ImageForm(ModelForm):

    class Meta:
        model = UploadedProfilePictures
        fields = ['image']