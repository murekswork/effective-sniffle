import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import CustomUser
from project_core.settings import STATIC_ROOT


class Interest(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    image = models.FileField(default='interests_covers/default_interest_cover.svg',
                             upload_to='interests_covers/')
    def __str__(self):
        return self.name


class Notification(models.Model):
    message = models.TextField(blank=False, default='Notification text', max_length=512)
    type = models.TextField(max_length='128')
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True, related_name='notifications')
    additional_profile = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)
    read_status = models.BooleanField(default=False)


    def create_unread_message_notification_text(self):
        self.message = f'{self.additional_profile} waits read from you!'
        return self.message

    def create_new_match_notification_text(self):
        self.message = f'You have matched with {self.additional_profile}'
        return self.message

    def __str__(self):
        return f'{self.recipient} - {self.type}'






class RelationFormatsModel(models.Model):

    name = models.CharField(max_length=64, default='Relation')
    about = models.CharField(max_length=512, default='About')
    image = models.ImageField(upload_to=f'relation_formats/{name}', blank=True)

    def __str__(self):
        return self.name


def create_user_path(instance, filename):
    return f'profiles_pics/user_{instance.profile_uploader.user_id}/{filename}'


class UploadedProfilePictures(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    profile_uploader = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, upload_to=create_user_path)





class Profile(models.Model):

    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]

    RELATION_FORMATS = [
        ('Hunter', 'Want to have some good time'),
        ('Love', 'Want to find real love'),
        ('Friend', 'Searching friends'),
        ('SE', 'Something Else')
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
    profile_main_picture = models.ForeignKey(UploadedProfilePictures, blank=True, null=True, on_delete=models.CASCADE)
    profile_uploaded_pictures = models.ManyToManyField(UploadedProfilePictures, null=True, blank=True, related_name='uploader')
    interests = models.ManyToManyField(Interest, blank=True, null=True)
    relation_formats = models.ForeignKey(RelationFormatsModel, on_delete=models.SET_NULL, null=True)

    def get_unread_notifications(self):
        unread_notifications = Notification.objects.filter(recipient=self, read_status=False)
        return unread_notifications

    def get_who_disliked_profiles(self):
        from like.models import DislikeModel
        who_disliked_profiles = DislikeModel.objects.filter(receiver=self).values_list('sender__user__id', flat=True)
        return who_disliked_profiles


    def get_liked_profiles(self):
        from like.models import LikeModel
        liked_profiles = LikeModel.objects.filter(sender=self).values_list('receiver__user__id', flat=True)
        return liked_profiles

    def get_disliked_profiles(self):
        from like.models import DislikeModel
        disliked_profiles = DislikeModel.objects.filter(sender=self).values_list('receiver__user__id', flat=True)
        return disliked_profiles


    def get_absolute_url(self):
        return reverse('profile', args=[str(self.user.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Create your models here.
