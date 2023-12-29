from django.contrib import admin
from .models import Profile, Interest, UploadedProfilePictures, RelationFormatsModel

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(UploadedProfilePictures)
admin.site.register(RelationFormatsModel)
# Register your models here.
