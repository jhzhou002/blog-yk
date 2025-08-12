from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category


class DashboardViewTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword'
        )

    def test_dashboard_home_requires_staff(self):
        # Test with regular user
        self.client.login(username='regularuser', password='testpassword')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_home_with_staff(self):
        # Test with staff user
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view(self):
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('dashboard:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_view(self):
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('dashboard:post_create'))
        self.assertEqual(response.status_code, 200)