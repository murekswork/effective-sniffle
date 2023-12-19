from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class Profile(models.Model):

    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=512, blank=True, editable=True)
    age = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    orientation = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Create your models here.
