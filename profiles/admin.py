from django.contrib import admin
from .models import Profile, Interest, UploadedProfilePictures

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(UploadedProfilePictures)
# Register your models here.
