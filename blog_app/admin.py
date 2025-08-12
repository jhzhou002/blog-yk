from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Category, Tag, Post, Comment, SiteSettings


# ==================== 用户和资料管理 ====================

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '用户资料'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# 重新注册User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'website', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']


# ==================== 博客内容管理 ====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'is_featured', 'published_at']
    list_filter = ['status', 'category', 'tags', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    ordering = ['-created_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('内容', {
            'fields': ('content', 'excerpt', 'cover_image')
        }),
        ('发布选项', {
            'fields': ('status', 'is_featured')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # 新建文章时自动设置作者
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_commenter_name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'name', 'email', 'user__username']
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "批准选中的评论"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "取消批准选中的评论"


# ==================== 网站设置管理 ====================

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