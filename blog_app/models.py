from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    """用户扩展资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.URLField('头像URL', blank=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)
    website = models.URLField('个人网站', blank=True)
    github = models.CharField('GitHub', max_length=100, blank=True)
    location = models.CharField('所在地', max_length=100, blank=True)
    birth_date = models.DateField('生日', null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} 的资料'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """用户保存时保存Profile"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Category(models.Model):
    """文章分类模型"""
    name = models.CharField('分类名', max_length=100, unique=True)
    slug = models.SlugField('URL标识', max_length=100, unique=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    """标签模型"""
    name = models.CharField('标签名', max_length=50, unique=True)
    slug = models.SlugField('URL标识', max_length=50, unique=True)
    color = models.CharField('颜色', max_length=7, default='#007bff')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    """文章模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField('标题', max_length=255)
    slug = models.SlugField('URL标识', max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    content = models.TextField('正文内容')
    excerpt = models.TextField('摘要', blank=True)
    cover_image = models.URLField('封面图URL', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField('推荐文章', default=False)
    views = models.PositiveIntegerField('阅读量', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:8]}")
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status == 'draft':
            self.published_at = None
        
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + '...' if len(self.content) > 200 else self.content
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_previous_post(self):
        return Post.objects.filter(
            status='published',
            published_at__lt=self.published_at
        ).first()

    def get_next_post(self):
        return Post.objects.filter(
            status='published',
            published_at__gt=self.published_at
        ).last()


class Comment(models.Model):
    """评论模型"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户')
    name = models.CharField('姓名', max_length=100, blank=True)
    email = models.EmailField('邮箱', blank=True)
    content = models.TextField('评论内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    is_approved = models.BooleanField('已审核', default=False)
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.get_commenter_name()} 对 "{self.post.title}" 的评论'

    def get_commenter_name(self):
        if self.user:
            return self.user.username
        return self.name or '匿名用户'


class SiteSettings(models.Model):
    """网站设置模型"""
    site_name = models.CharField('网站名称', max_length=100, default='个人博客')
    site_description = models.TextField('网站描述', blank=True)
    site_keywords = models.CharField('SEO关键词', max_length=200, blank=True)
    site_author = models.CharField('网站作者', max_length=100, blank=True)
    site_logo = models.URLField('网站Logo', blank=True)
    favicon = models.URLField('网站图标', blank=True)
    footer_text = models.TextField('页脚文本', blank=True)
    
    # 社交媒体链接
    github_url = models.URLField('GitHub链接', blank=True)
    weibo_url = models.URLField('微博链接', blank=True)
    wechat_qr = models.URLField('微信二维码', blank=True)
    
    # 统计代码
    google_analytics = models.TextField('Google Analytics代码', blank=True)
    baidu_statistics = models.TextField('百度统计代码', blank=True)
    
    # 评论设置
    comment_moderation = models.BooleanField('评论审核', default=True)
    allow_anonymous_comments = models.BooleanField('允许匿名评论', default=False)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = '网站设置'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        """获取网站设置（单例模式）"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings