from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, ListView

from like.models import Match, LikeModel
from .mixins import ProfileRequiredMixin
from .models import Profile, Interest, UploadedProfilePictures, Notification
from .forms import ProfileCreationForm, ImageForm


class ProfileCreationView(LoginRequiredMixin, CreateView):
    form_class = ProfileCreationForm
    model = Profile
    template_name = 'profiles/profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
# Create your views here.

class ProfileNotificationsView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    template_name = 'profiles/notifications.html'
    model = Notification
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        context = {}
        context['notifications'] = self.get_queryset()
        context['unread_notifications'] = context['notifications']
        context['notifications'].update(read_status=True)
        return render(request, self.template_name, context)

class ProfileActivityMatchesView(TemplateView):
    template_name = 'profile/activity.html'





def profile_set_new_photo(request, pk):
    picture = UploadedProfilePictures.objects.get(id=pk)
    request_profile = request.user.profile
    if picture in request_profile.profile_uploaded_pictures.select_related():
            request_profile.profile_main_picture = picture
            request_profile.save()
    return redirect(request.META.get('HTTP_REFERER'))





class ProfileOverviewView(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):
    template_name = 'profiles/profile_overview.html'


    def get_context_data(self, **kwargs):
        request_profile = self.request.user.profile

        return {'profile': request_profile,
                'form': ImageForm}

    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES:
            image_instance = form.save(commit=False)
            image_instance.profile_uploader = request.user.profile
            image_instance.save()
            request.user.profile.profile_uploaded_pictures.add(image_instance)
            with open('image_save_logs.txt', 'w+') as f:
                f.write(str(image_instance))
        return redirect(request.META.get('HTTP_REFERER'))


class ProfileUpdateView(LoginRequiredMixin, ProfileRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile_overview')
    template_name = 'profiles/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile



class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'


class ProfileActivityMatchesView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'profiles/activity/activity_matches.html'

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = Match.objects.filter(Q(profile1=user_profile) | Q(profile2=user_profile))
        return queryset


class ProfileActivitySentLikesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/activity/activity_sent_likes.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = LikeModel.objects.filter(sender_id=self.request.user.id).values('receiver')
        profiles_set = [Profile.objects.get(user_id=i['receiver']) for i in queryset]
        return profiles_set

class ProfileActivityReceivedLikesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/activity/activity_received_likes.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = LikeModel.objects.filter(receiver_id=self.request.user.id).values('sender')
        profiles_set = [Profile.objects.get(user_id=i['sender']) for i in queryset]
        return profiles_set









