from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, ListView

from like.models import Match, LikeModel
from .mixins import ProfileRequiredMixin
from .models import Profile, Interest, UploadedProfilePictures
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


class ProfileMatchesView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'profiles/profile_matches.html'

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = Match.objects.filter(Q(profile1=user_profile) | Q(profile2=user_profile))
        return queryset









