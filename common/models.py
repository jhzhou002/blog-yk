from django.db import models


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