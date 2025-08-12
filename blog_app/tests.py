from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment, Profile, SiteSettings


class ModelTests(TestCase):
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

    def test_profile_creation_on_user_creation(self):
        """测试用户创建时自动创建Profile"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_post_creation(self):
        """测试文章创建"""
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
        """测试分类字符串表示"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_post_absolute_url(self):
        """测试文章绝对URL"""
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            status='published'
        )
        expected_url = reverse('post_detail', kwargs={'slug': post.slug})
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_site_settings_singleton(self):
        """测试网站设置单例模式"""
        settings1 = SiteSettings.get_settings()
        settings2 = SiteSettings.get_settings()
        self.assertEqual(settings1.pk, settings2.pk)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword',
            is_staff=True
        )

    def test_home_view(self):
        """测试首页视图"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        """测试文章详情视图"""
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            status='published'
        )
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_register_view_get(self):
        """测试注册页面GET请求"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        """测试登录页面GET请求"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_staff(self):
        """测试管理面板需要管理员权限"""
        # 未登录用户
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)  # 重定向到登录页

        # 普通用户
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)  # 重定向到登录页

        # 管理员用户
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """测试用户注册功能"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # 注册成功后重定向
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_search_functionality(self):
        """测试搜索功能"""
        post = Post.objects.create(
            title='Searchable Post',
            content='This post should be found in search',
            author=self.user,
            status='published'
        )
        
        response = self.client.get(reverse('search'), {'q': 'Searchable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)


class FormTests(TestCase):
    def test_comment_form(self):
        """测试评论表单"""
        from .forms import CommentForm
        
        form_data = {'content': 'This is a test comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form(self):
        """测试用户注册表单"""
        from .forms import CustomUserCreationForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())