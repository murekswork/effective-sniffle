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
	user_block_decision = models.BooleanField(blank=True, default=False)
	decision_explanation = models.TextField(blank=True, default='Just because!')

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


	def take_decision(self, **kwargs):
		self.decision_explanation = kwargs['decision_explanation']
		self.status = True
		if kwargs['user_block_decision']:
			self.user_block_decision = True
			self.receiver.is_active = False
			profile = self.receiver.profile
			profile.first_name = 'Profile'
			profile.last_name = 'is blocked!'
			## --! Removing moderator from complain receiver chats !--##
			chats = profile.chat_set.select_related()
			for chat in chats:
				chat.profile.remove(self.responsible_moderator.profile)
	
			profile.save()
			self.receiver.save()
		self.save()
		return {'user_blocked': self.user_block_decision, 'decision_explanation': self.decision_explanation}

	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('complain', args=[str(self.id)])
