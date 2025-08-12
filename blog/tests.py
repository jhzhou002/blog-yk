from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Tag, Post


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.status, 'published')
        self.assertTrue(post.slug)

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_post_absolute_url(self):
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            status='published'
        )
        expected_url = reverse('blog:post_detail', kwargs={'slug': post.slug})
        self.assertEqual(post.get_absolute_url(), expected_url)


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_home_view(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            status='published'
        )
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)