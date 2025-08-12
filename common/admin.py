from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_author', 'comment_moderation', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('site_name', 'site_description', 'site_keywords', 'site_author')
        }),
        ('视觉设计', {
            'fields': ('site_logo', 'favicon', 'footer_text')
        }),
        ('社交媒体', {
            'fields': ('github_url', 'weibo_url', 'wechat_qr')
        }),
        ('统计代码', {
            'fields': ('google_analytics', 'baidu_statistics')
        }),
        ('评论设置', {
            'fields': ('comment_moderation', 'allow_anonymous_comments')
        }),
    )
    
    def has_add_permission(self, request):
        # 只允许存在一个设置实例
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # 不允许删除设置
        return False