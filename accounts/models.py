import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	is_moderator = models.BooleanField(default=False)

	def set_moderator(self):
		self.is_moderator = True
		self.save()
		return self.is_moderator
# Create your models here.
