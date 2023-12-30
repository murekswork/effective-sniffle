from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from profiles.models import Profile
from .views import PublicPageView

class TestDates(TestCase):

    def setUp(self):
        user = CustomUser.objects.create_user(email='dates_test_user@email.com', username='dates_user', password='0xABAD1DEA')
        self.client.login(email='dates_test_user@email.com', password='0xABAD1DEA')
        User = self.client.get(reverse('profile_overview')).context['request'].user
        self.profile = Profile.objects.create(user=User, first_name='MainTestUserM', last_name='Test', gender='M', orientation='F')

        TEST_PROFILES_EMAIL_USERNAMES_F = [('test_email@email.com', 'username_test1'),
                                         ('test1_email@email.com', 'username_test2'),
                                         ('test2@email.com', 'username_test3')]
        TEST_USERS_F = (CustomUser.objects.create_user(email=i[0], username=i[1], password='0xABAD1DEA') for i in
                        TEST_PROFILES_EMAIL_USERNAMES_F)

        TEST_PROFILES_F = [
            Profile.objects.get_or_create(user=USER_F, first_name=f'{USER_F.email}', last_name='test', gender='F',
                                          orientation='M') for USER_F in TEST_USERS_F]

        TEST_PROFILES_EMAIL_USERNAMES_M = [('test_email_m@email.com', 'username_test1_m'),
                                         ('test1_email_m@email.com', 'username_test2_m'),
                                         ('test2_email_m@email.com', 'username_test3_m')]
        TEST_USERS_M = (CustomUser.objects.create_user(email=i[0], username=i[1], password='0xABAD1DEA') for i in
                        TEST_PROFILES_EMAIL_USERNAMES_M)

        TEST_PROFILES_M = [
            Profile.objects.get_or_create(user=USER_M, first_name=f'{USER_M.email}', last_name='test', gender='M',
                                          orientation='F') for USER_M in TEST_USERS_M]

    def test_public_page_view_as_male_orientation_female(self):
        self.client.login(email='dates_test_user@email.com', password='0xABAD1DEA')
        response = self.client.get(reverse('public'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test1_email@email.com')
        self.assertNotContains(response, 'MainTestUser')
        self.assertNotContains(response, 'test_email_m@email.com')
        self.assertTemplateUsed(response, 'dates/public.html')
        self.assertEqual(response.resolver_match.func.__name__, PublicPageView.as_view().__name__)

    def test_public_page_view_as_female_orientation_male(self):
        self.client.login(email='dates_test_user@email.com', password='0xABAD1DEA')
        self.profile.gender = 'F'
        self.profile.orientation = 'M'
        self.profile.save()
        response = self.client.get(reverse('public'))
        print(self.profile.gender, self.profile.orientation)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_email_m@email.com')
        self.assertNotContains(response, 'test_email@email.com')
        self.assertTemplateUsed(response, 'dates/public.html')
        self.assertEqual(response.resolver_match.func.__name__, PublicPageView.as_view().__name__)



# Create your tests here.
