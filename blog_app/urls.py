from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 博客首页和文章
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search, name='search'),
    path('archive/', views.archive, name='archive'),
    path('archive/<int:year>/<int:month>/', views.archive_month, name='archive_month'),
    path('post/<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    
    # 用户认证
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # 密码重置
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # 密码修改
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html'
         ), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ), 
         name='password_change_done'),
    
    # 管理面板
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/posts/', views.post_list, name='post_list'),
    path('dashboard/comments/', views.comment_list, name='comment_list'),
    path('dashboard/comments/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('dashboard/comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]