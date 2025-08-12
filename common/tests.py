from django.test import TestCase
from .models import SiteSettings
from .utils import truncate_text, generate_unique_slug
from blog.models import Post


class CommonUtilsTests(TestCase):
    def test_truncate_text(self):
        text = "This is a long text that should be truncated"
        result = truncate_text(text, 20)
        self.assertTrue(len(result) <= 23)  # 20 chars + "..."
        self.assertTrue(result.endswith('...'))

    def test_truncate_text_short(self):
        text = "Short text"
        result = truncate_text(text, 20)
        self.assertEqual(result, text)

    def test_generate_unique_slug(self):
        slug = generate_unique_slug(Post, "Test Title")
        self.assertTrue(slug)
        self.assertIsInstance(slug, str)


class SiteSettingsTests(TestCase):
    def test_site_settings_singleton(self):
        settings1 = SiteSettings.get_settings()
        settings2 = SiteSettings.get_settings()
        self.assertEqual(settings1.pk, settings2.pk)

    def test_site_settings_defaults(self):
        settings = SiteSettings.get_settings()
        self.assertEqual(settings.site_name, '个人博客')
        self.assertTrue(settings.comment_moderation)