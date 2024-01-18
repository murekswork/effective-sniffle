from django.db import models
from project_core import settings
from django.contrib.auth import get_user_model
from profiles.models import Profile

class ProfileLocation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    latitude = models.CharField(blank=False, null=True, max_length=25)

    def __str__(self):
        return f'{self.user} - {self.latitude} - {self.longitude}'


class LocationProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    latitude = models.CharField(blank=False, null=True, max_length=25)
    longitude = models.CharField(blank=False, null=True, max_length=25)

    def __str__(self):
        return f'{self.user} - {self.latitude} - {self.longitude}'




# Create your models here.
