from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class AccountsModelTests(TestCase):
    def test_profile_creation_on_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

    def test_profile_str_method(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        expected_str = f'{user.username} 的资料'
        self.assertEqual(str(user.profile), expected_str)


class AccountsViewTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())