from django.db import models
from profiles.models import Profile


class Match(models.Model):
    profile1 = models.ForeignKey(Profile, blank=True, on_delete=models.CASCADE, related_name='match_profile1')
    profile2 = models.ForeignKey(Profile, blank=True, null=False, on_delete=models.CASCADE, related_name='match_profile2')
    matched_at = models.DateTimeField(auto_now_add=True)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return F"{self.profile1} matched {self.profile2}"


class DislikeModel(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='send_dislikes')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dislikes')
    disliked_at = models.DateTimeField(auto_now_add=True)


class LikeModel(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='like_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='like_receiver')
    liked_at = models.DateTimeField(auto_now_add=True)





    @staticmethod
    def check_like(sender, receiver):
        like = LikeModel.objects.filter(sender=sender, receiver=receiver).select_related()
        if not like:
            return False
        return True










# Create your models here.
