from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Complain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
import random
from .forms import ComplainForm
from django.http import JsonResponse
## --! Make this function work
def get_responsible_moderator():
	return random.choice(list(get_user_model().objects.filter(is_moderator=True)))


class ModeratorPageView(LoginRequiredMixin, UserPassesTestMixin, View):

	template_name = 'account/moderating/moderator_page.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def test_func(self):
		return self.request.user.is_moderator

	def get_context_data(self, **kwargs):
		context = dict()
		context['complains'] = Complain.objects.filter(responsible_moderator=self.request.user)
		return context


class ComplainPageView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Complain
	template_name = 'account/moderating/complain.html'
	context_object_name = 'complain'

	def get(self, request, *args, **kwargs):
		context = dict()
		context['complain'] = self.get_object()
		if not context['complain'].moderator_chat_access():
			context['receiver_chats'] = context['complain'].give_moderator_receiver_chats_access()
		context['receiver_chats'] = context['complain'].receiver.profile.chat_set.select_related()
		return render(request, self.template_name, context)


	def test_func(self):
		return self.request.user == self.get_object().responsible_moderator


class AjaxSendComplainView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return JsonResponse({'message': "form send"})

	def post(self, request, *args, **kwargs):
		reason = request.POST.get('reason')
		description = request.POST.get('description')
		profile_pk = request.POST.get('profile_pk')
		sender = request.user
		receiver = get_user_model().objects.get(pk=profile_pk)

		complain = Complain(sender=sender, receiver=receiver, reason=reason, description=description, responsible_moderator=get_responsible_moderator())
		complain.save()
		return JsonResponse({'message': 'Your complain successfully saved!', 'report_id': complain.id})


	

# Create your views here.
