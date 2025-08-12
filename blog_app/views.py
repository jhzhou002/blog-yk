from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, F, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, Profile, SiteSettings
from .forms import (CommentForm, CustomUserCreationForm, UserUpdateForm, 
                   ProfileUpdateForm, CustomLoginForm, PostForm, CategoryForm, 
                   TagForm, SiteSettingsForm)
import json


# ==================== 博客首页和文章视图 ====================

def home(request):
    """首页视图"""
    try:
        posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        featured_posts = Post.objects.filter(status='published', is_featured=True)[:5]
        popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
        latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:5]
        categories = Category.objects.all()
        tags = Tag.objects.all()[:20]
        
        context = {
            'page_obj': page_obj,
            'featured_posts': featured_posts,
            'popular_posts': popular_posts,
            'latest_posts': latest_posts,
            'categories': categories,
            'tags': tags,
        }
    except Exception as e:
        # 如果数据库表不存在，显示安装页面
        context = {
            'page_obj': None,
            'featured_posts': [],
            'popular_posts': [],
            'latest_posts': [],
            'categories': [],
            'tags': [],
            'db_error': True,
            'error_message': '数据库表尚未创建，请先运行数据库迁移命令。'
        }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    """文章详情页"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()
    
    comments = Comment.objects.filter(
        post=post, 
        is_approved=True, 
        parent__isnull=True
    ).select_related('user').prefetch_related('replies__user')
    
    comment_form = CommentForm()
    previous_post = post.get_previous_post()
    next_post = post.get_next_post()
    
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(pk=post.pk)[:4]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'previous_post': previous_post,
        'next_post': next_post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    """分类详情页"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    """标签详情页"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_detail.html', context)


def search(request):
    """搜索功能"""
    query = request.GET.get('q', '').strip()
    posts = []
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': posts.count() if query else 0,
    }
    return render(request, 'blog/search_results.html', context)


def archive(request):
    """文章归档页"""
    posts = Post.objects.filter(status='published').dates('published_at', 'month', order='DESC')
    
    archive_data = []
    for date in posts:
        month_posts = Post.objects.filter(
            status='published',
            published_at__year=date.year,
            published_at__month=date.month
        ).count()
        archive_data.append({
            'date': date,
            'count': month_posts
        })
    
    context = {
        'archive_data': archive_data,
    }
    return render(request, 'blog/archive.html', context)


def archive_month(request, year, month):
    """月份归档详情"""
    posts = Post.objects.filter(
        status='published',
        published_at__year=year,
        published_at__month=month
    )
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'year': year,
        'month': month,
        'page_obj': page_obj,
    }
    return render(request, 'blog/archive_month.html', context)


@login_required
@require_POST
def add_comment(request, post_slug):
    """添加评论"""
    post = get_object_or_404(Post, slug=post_slug, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.ip_address = get_client_ip(request)
        
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                comment.parent_id = int(parent_id)
            except (ValueError, TypeError):
                pass
        
        comment.save()
        messages.success(request, '评论提交成功，等待审核后显示。')
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': '评论提交成功'})
    else:
        messages.error(request, '评论提交失败，请检查输入内容。')
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return redirect('post_detail', slug=post_slug)


# ==================== 用户认证视图 ====================

class CustomLoginView(LoginView):
    """自定义登录视图"""
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def register(request):
    """用户注册"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户创建成功！欢迎 {username}！')
            
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """用户资料页面"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """编辑用户资料"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '您的资料已成功更新！')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


# ==================== 管理面板视图 ====================

@staff_member_required
def dashboard_home(request):
    """管理面板首页"""
    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'total_comments': Comment.objects.count(),
        'pending_comments': Comment.objects.filter(is_approved=False).count(),
        'total_users': User.objects.count(),
        'total_categories': Category.objects.count(),
        'total_tags': Tag.objects.count(),
    }
    
    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
    recent_comments = Comment.objects.select_related('post', 'user').order_by('-created_at')[:5]
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'popular_posts': popular_posts,
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def post_list(request):
    """文章列表管理"""
    posts = Post.objects.select_related('author', 'category').prefetch_related('tags')
    
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search)
        )
    
    status = request.GET.get('status')
    if status:
        posts = posts.filter(status=status)
    
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category_id=category)
    
    posts = posts.order_by('-created_at')
    
    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_search': search,
        'current_status': status,
        'current_category': category,
    }
    return render(request, 'dashboard/post_list.html', context)


@staff_member_required
def comment_list(request):
    """评论管理"""
    comments = Comment.objects.select_related('post', 'user').order_by('-created_at')
    
    approved = request.GET.get('approved')
    if approved == 'true':
        comments = comments.filter(is_approved=True)
    elif approved == 'false':
        comments = comments.filter(is_approved=False)
    
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_approved': approved,
    }
    return render(request, 'dashboard/comment_list.html', context)


@staff_member_required
def comment_approve(request, pk):
    """批准评论"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = True
        comment.save()
        messages.success(request, '评论已批准！')
    
    return redirect('comment_list')


@staff_member_required
def comment_delete(request, pk):
    """删除评论"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        messages.success(request, '评论已删除！')
    
    return redirect('comment_list')


# ==================== 工具函数 ====================

def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip