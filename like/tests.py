from django.test import TestCase
from accounts.models import CustomUser
from profiles.models import Profile
from like.models import Match, LikeModel
from django.db.models import Q


class MatchTests(TestCase):

    def setUp(self):
        user1 = CustomUser.objects.create_user(email='user1@mail.com', username='USER1', password='0xABAD1DEA')
        user2 = CustomUser.objects.create_user(email='user2@mail.com', username='USER2', password='0xABAD1DEA')
        self.profile1 = Profile.objects.create(user=user1, first_name='User1', last_name='Last1', orientation='M', gender='M')
        self.profile2 = Profile.objects.create(user=user2, first_name='User2', last_name='Last2', orientation='F', gender='F')

    def test_match_creation(self):
        MATCH = Match.objects.create(profile1=self.profile1, profile2=self.profile2)
        self.assertEqual(MATCH.profile1.first_name, 'User1')
        self.assertEqual(MATCH.profile2.first_name, 'User2')

    def test_likes_model(self):
        like1 = LikeModel.objects.create(sender=self.profile1, receiver=self.profile2)
        match = like1.check_like_from_receiver()
        self.assertEqual(match, 'NOT MATCH')
        self.assertNotEquals(match, 'MATCH')
        self.assertFalse(Match.objects.filter(Q(profile1=self.profile1, profile2=self.profile2) | Q(profile1=self.profile2, profile2=self.profile1)))
        like2 = LikeModel.objects.create(sender=self.profile2, receiver=self.profile1)
        match = like2.check_like_from_receiver()
        self.assertTrue(Match.objects.filter(Q(profile1=self.profile1, profile2=self.profile2) | Q(profile1=self.profile2, profile2=self.profile1)))


# Create your tests here.
