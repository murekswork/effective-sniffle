from django.shortcuts import render, redirect

from django.views.generic import DetailView, View
from .models import Complain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
import random
from .forms import ComplainForm, ComplainDecisionForm
from django.http import JsonResponse
## --! Make this function work
def get_responsible_moderator():
	return random.choice(list(get_user_model().objects.filter(is_moderator=True)))


class ModeratorsControlPageView(LoginRequiredMixin, UserPassesTestMixin, View):

	template_name = 'account/moderating/moderators_control.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, context=self.get_context_data(**kwargs))
	def get_context_data(self, **kwargs):
		context = dict()
		context['moderators'] = get_user_model().objects.filter(is_moderator=True)
		return context

	def test_func(self):
		return self.request.user.is_superuser

class ModeratorPageView(LoginRequiredMixin, UserPassesTestMixin, View):

	template_name = 'account/moderating/moderator_page.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def test_func(self):
		return self.request.user.is_moderator

	def get_context_data(self, **kwargs):
		context = dict()
		context['complains'] = Complain.objects.filter(responsible_moderator=self.request.user).order_by('status')
		return context


class ComplainPageView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Complain
	template_name = 'account/moderating/complain.html'
	context_object_name = 'complain'

	def get_context_data(self, **kwargs):
		context = dict()
		complain = context['complain'] = self.get_object()
		if not complain.moderator_chat_access():
			complain.give_moderator_receiver_chats_access()
		context['receiver_chats'] = complain.receiver.profile.chat_set.select_related()
		context['form'] = ComplainDecisionForm
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		decision_explanation = request.POST.get('decision_explanation')
		user_block_decision = request.POST.get('user_block_decision')
		complain = self.get_object()
		complain.take_decision(decision_explanation=decision_explanation, user_block_decision=user_block_decision)
		return redirect(request.META.get('HTTP_REFERER'))



	def test_func(self):
		return self.request.user == self.get_object().responsible_moderator or self.request.user.is_superuser


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
