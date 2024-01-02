from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile, UploadedProfilePictures

from .bots_logic import create_name, create_username_by_name
from django.urls import reverse
import random


class Bot(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=120, default='0xABAD1DEA')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def delete(self):
        super().delete()
        self.profile.delete()
        self.user.delete()

    def create_bot_user(self):
        name = create_name()
        username = create_username_by_name(name)
        password = '0xABAD1DEA'
        new_user = get_user_model().objects.create_user(username=username, password=password, email=f'{username}@bot.com')
        new_user.save()
        self.user = new_user
        return new_user

    def create_bot_profile(self, **kwargs):
        gender = kwargs.get('gender')
        orientation = kwargs.get('orientation')
        bot_profile = Profile.objects.create(user=self.user, first_name=create_name(), last_name='bot',
                                             gender=gender, orientation=orientation)
        bot_profile.save()
        self.profile = bot_profile

    def get_bot_data(self):
        data = (f'username: {self.user.username}, email: {self.user.email} \n'
                f'first_name: {self.profile.first_name}, last_name: {self.profile.last_name} \n'
                f'gender: {self.profile.gender}')
        return data

    def update_profile_photo(self):
        random_photo = random.choice(UploadedProfilePictures.objects.all())
        self.profile.profile_main_picture = random_photo
        self.profile.save()

    def get_absolute_url(self):
        return reverse('bot_page', args=[str(self.id)])

    def __str__(self):
        if self.profile:
            return str(self.profile)
        if self.user:
            return str(self.user)
        return str(self.id)


# Create your models here.
