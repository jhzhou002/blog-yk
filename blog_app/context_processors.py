from .models import SiteSettings, Category, Tag


def site_settings(request):
    """全局网站设置上下文处理器"""
    settings = SiteSettings.get_settings()
    return {
        'site_settings': settings
    }


def navigation_context(request):
    """导航相关上下文处理器"""
    categories = Category.objects.all()[:10]  # 最多显示10个分类
    popular_tags = Tag.objects.all()[:20]     # 最多显示20个标签
    
    return {
        'nav_categories': categories,
        'nav_tags': popular_tags,
    }