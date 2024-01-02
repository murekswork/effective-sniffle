from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile, UploadedProfilePictures

from .bots_logic import create_name, create_username_by_name
from django.urls import reverse


class Bot(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=120, default='0xABAD1DEA')
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def create_bot_user(self):
        name = create_name()
        username = create_username_by_name(name)
        password = '0xABAD1DEA'
        new_user = get_user_model().objects.create_user(username=username, password=password, email=f'{username}@bot.com')
        new_user.save()
        self.user = new_user

    def create_bot_profile(self):
        bot_profile = Profile.objects.create(user=self.user, first_name=create_name(), last_name='bot')
        bot_profile.save()
        self.profile = bot_profile

    def get_bot_data(self):
        data = (f'username: {self.user.username}, email: {self.user.email} \n'
                f'first_name: {self.profile.first_name}, last_name: {self.profile.last_name} \n'
                f'gender: {self.profile.gender}' )
        return data

    def set_bot_profile_picture(self):
        photo = UploadedProfilePictures.objects.create(profile_uploader=self.profile, image='relation.jpg')
        photo.save()
        self.profile.profile_main_picture = photo

    def get_absolute_url(self):
        return reverse('bot_page', args=[str(self.id)])

    def __str__(self):
        if self.profile:
            return str(self.profile)
        if self.user:
            return str(self.user)
        return str(self.id)


# Create your models here.
