import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from accounts.models import CustomUser
from .models import Profile
from .views import ProfileCreationView, ProfileOverviewView, ProfileUpdateView, ProfileView


class ProfileTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='testuser@email.com',
            username='testuser1',
            password='0xABAD1DEA'
        )


    def test_not_authenticated_user_profile_creation_access(self):
        response = self.client.get(reverse('profile_create'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_profile_creation_access(self):
        self.client.login(email='testuser@email.com', password='0xABAD1DEA')
        response = self.client.get(reverse('profile_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ProfileCreationView.as_view().__name__)
        self.assertTemplateUsed(response, template_name='profiles/profile_create.html')
        self.assertContains(response, 'Create your profile')

    def test_access_not_authenticated_user_profile_overview_template(self):
        self.client.logout()
        response = self.client.get(reverse('profile_overview'))
        self.assertEqual(response.status_code, 302)

    def test_access_authenticated_user_profile_overview_template(self):
        self.client.login(email='testuser@email.com', password='0xABAD1DEA')
        response = self.client.get(reverse('profile_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile overview')
        self.assertTemplateUsed(response, 'profiles/profile_overview.html')
        view = response.resolver_match
        self.assertEqual(view.func.__name__, ProfileOverviewView.as_view().__name__)

    def test_access_not_authenticated_user_profile_update_template(self):
        self.client.logout()
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 302)

    def test_access_authenticated_user_with_not_profile_update_template(self):
        self.client.login(email='testuser@email.com', password='0xABAD1DEA')
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 302)

    def test_access_authenticated_user_with_profile_update_template(self):
        self.client.login(email='testuser@email.com', password='0xABAD1DEA')
        User = self.client.get(reverse('profile_overview')).context['request'].user
        profile = Profile.objects.create(first_name='Test', last_name='User',
                                         user=User, gender='M',
                                         orientation='F')
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile update')
        self.assertTemplateUsed(response, 'profiles/profile_update.html')
        view = response.resolver_match
        self.assertEqual(view.func.__name__, ProfileUpdateView.as_view().__name__)

    def test_profile_view(self):
        self.client.login(email='testuser@email.com', password='0xABAD1DEA')
        User = self.client.get(reverse('profile_overview')).context['request'].user
        profile = Profile.objects.create(first_name='Test', last_name='User',
                                         user=User, gender='M',
                                         orientation='F')
        User1 = CustomUser.objects.create_user(email='user1@mail.com',
                                               username='user1',
                                               password='0xABAD1DEA')
        profile1 = Profile.objects.create(first_name='Contain', last_name='Test',
                                         user=User1, gender='M',
                                         orientation='F')
        response = self.client.get(profile1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profiles/profile.html')
        self.assertContains(response, 'Contain')
        self.assertEqual(response.resolver_match.func.__name__, ProfileView.as_view().__name__)



# Create your tests here.
