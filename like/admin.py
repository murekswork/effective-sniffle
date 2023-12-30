from django.contrib import admin

from like.models import Match, LikeModel, DislikeModel

admin.site.register(Match)
admin.site.register(LikeModel)
admin.site.register(DislikeModel)

# Register your models here.
