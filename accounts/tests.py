from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model

class TestCustomUser(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='testuser1',
                                        email='testuser1password@mail.com',
                                        password='0xABAD1DEA')

    def test_default_user(self):
        self.assertEqual(self.user.username, 'testuser1')
        self.assertEqual(self.user.email, 'testuser1password@mail.com')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_super_user(self):
        UserAdmin = get_user_model()
        user_admin = UserAdmin.objects.create_superuser(username='useradmin',
                                                        email='useradmin@mail.com',
                                                        password='useradminpassword123')
        self.assertEqual(user_admin.username, 'useradmin')
        self.assertEqual(user_admin.email, 'useradmin@mail.com')
        self.assertTrue(user_admin.is_superuser)
        self.assertTrue(user_admin.is_staff)
        self.assertTrue(user_admin.is_active)



# Create your tests here.
