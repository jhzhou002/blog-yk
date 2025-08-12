from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blog.models import Post, Category, Tag, Comment
from accounts.models import Profile
from common.models import SiteSettings
from django.contrib.auth.models import User
from .forms import PostForm, CategoryForm, TagForm


@staff_member_required
def dashboard_home(request):
    """管理面板首页"""
    # 统计数据
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
    
    # 最近的文章
    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
    
    # 最近的评论
    recent_comments = Comment.objects.select_related('post', 'user').order_by('-created_at')[:5]
    
    # 热门文章
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
    
    # 搜索功能
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search)
        )
    
    # 状态筛选
    status = request.GET.get('status')
    if status:
        posts = posts.filter(status=status)
    
    # 分类筛选
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category_id=category)
    
    posts = posts.order_by('-created_at')
    
    # 分页
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
def post_create(request):
    """创建文章"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # 保存多对多关系（标签）
            messages.success(request, '文章创建成功！')
            return redirect('dashboard:post_list')
    else:
        form = PostForm()
    
    return render(request, 'dashboard/post_form.html', {
        'form': form,
        'title': '创建文章'
    })


@staff_member_required
def post_edit(request, pk):
    """编辑文章"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('dashboard:post_list')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'dashboard/post_form.html', {
        'form': form,
        'post': post,
        'title': '编辑文章'
    })


@staff_member_required
def post_delete(request, pk):
    """删除文章"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '文章删除成功！')
        return redirect('dashboard:post_list')
    
    return render(request, 'dashboard/post_confirm_delete.html', {'post': post})


@staff_member_required
def comment_list(request):
    """评论管理"""
    comments = Comment.objects.select_related('post', 'user').order_by('-created_at')
    
    # 审核状态筛选
    approved = request.GET.get('approved')
    if approved == 'true':
        comments = comments.filter(is_approved=True)
    elif approved == 'false':
        comments = comments.filter(is_approved=False)
    
    # 分页
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
    
    return redirect('dashboard:comment_list')


@staff_member_required
def comment_disapprove(request, pk):
    """取消批准评论"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = False
        comment.save()
        messages.success(request, '评论已取消批准！')
    
    return redirect('dashboard:comment_list')


@staff_member_required
def comment_delete(request, pk):
    """删除评论"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        messages.success(request, '评论已删除！')
    
    return redirect('dashboard:comment_list')


@staff_member_required
def category_list(request):
    """分类管理"""
    categories = Category.objects.annotate(
        post_count=Count('post')
    ).order_by('name')
    
    return render(request, 'dashboard/category_list.html', {
        'categories': categories
    })


@staff_member_required
def category_create(request):
    """创建分类"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '分类创建成功！')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'title': '创建分类'
    })


@staff_member_required
def category_edit(request, pk):
    """编辑分类"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '分类更新成功！')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'category': category,
        'title': '编辑分类'
    })


@staff_member_required
def tag_list(request):
    """标签管理"""
    tags = Tag.objects.annotate(
        post_count=Count('post')
    ).order_by('name')
    
    return render(request, 'dashboard/tag_list.html', {
        'tags': tags
    })


@staff_member_required
def site_settings(request):
    """网站设置"""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        # 这里可以添加表单处理逻辑
        messages.success(request, '设置保存成功！')
        return redirect('dashboard:site_settings')
    
    return render(request, 'dashboard/site_settings.html', {
        'settings': settings
    })