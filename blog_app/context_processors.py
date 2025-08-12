from .models import SiteSettings, Category, Tag


def site_settings(request):
    """全局网站设置上下文处理器"""
    try:
        settings = SiteSettings.get_settings()
        return {
            'site_settings': settings
        }
    except Exception:
        # 如果数据库表不存在，返回默认设置
        class DefaultSettings:
            site_name = "个人博客"
            site_description = "基于Django的响应式博客系统"
            site_keywords = "博客,Django,Python"
            site_author = "博客作者"
            site_logo = ""
            favicon = ""
            footer_text = ""
            github_url = ""
            weibo_url = ""
            wechat_qr = ""
        
        return {
            'site_settings': DefaultSettings()
        }


def navigation_context(request):
    """导航相关上下文处理器"""
    try:
        categories = Category.objects.all()[:10]  # 最多显示10个分类
        popular_tags = Tag.objects.all()[:20]     # 最多显示20个标签
        
        return {
            'nav_categories': categories,
            'nav_tags': popular_tags,
        }
    except Exception:
        # 如果数据库表不存在，返回空列表
        return {
            'nav_categories': [],
            'nav_tags': [],
        }