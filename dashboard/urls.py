from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # 管理面板首页
    path('', views.dashboard_home, name='home'),
    
    # 文章管理
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    # 评论管理
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comments/<int:pk>/disapprove/', views.comment_disapprove, name='comment_disapprove'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    
    # 分类管理
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    
    # 标签管理
    path('tags/', views.tag_list, name='tag_list'),
    
    # 网站设置
    path('settings/', views.site_settings, name='site_settings'),
]