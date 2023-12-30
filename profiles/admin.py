from django.contrib import admin
from .models import Profile, Interest, UploadedProfilePictures, RelationFormatsModel, Notification

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(UploadedProfilePictures)
admin.site.register(RelationFormatsModel)
admin.site.register(Notification)
# Register your models here.
