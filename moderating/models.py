from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Complain(models.Model):
	
	COMPLAIN_REASONS = (('REASON1', '1111111111111'), ('REASON2', '22222222'), ('REASON3', '333333333'))

	sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True, related_name='user_complains')
	receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
	reason = models.CharField(choices=COMPLAIN_REASONS, max_length=255, blank=True, null=True)
	time = models.DateTimeField(auto_now_add=True)
	responsible_moderator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='complains_responsible')
	description = models.TextField(blank=True, null=True)

	# --! Status: 0 means that moderator didnt take decision yet and 1 means it took
	status = models.BooleanField(default=False)

	# --! Decision: 0 means that user is innocent and 1 means that user bad
	decision = models.BooleanField(blank=True, default=False)

	def moderator_chat_access(self):
		receiver_chats = self.receiver.profile.chat_set.select_related()
		if not receiver_chats:
			return {'error': 'receiver has not chats'}
		if self.responsible_moderator.profile in [self.receiver.profile.chat_set.select_related()[0].profiles]:
			return True
		return False

	def give_moderator_receiver_chats_access(self):
		receiver_chats = self.receiver.profile.chat_set.select_related()
		for receiver_chat in receiver_chats:
			receiver_chat.profiles.add(self.responsible_moderator.profile)
		return receiver_chats


	def take_decision(self, kwargs):
		self.decision = True
		if kwargs['decision'] == 'block_receiver':
			return {'decision': 'user blocked!'}
		return {'decision': 'user not blocked! thanks for you attention!'}

	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('complain', args=[str(self.id)])
