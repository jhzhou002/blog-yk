from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
import json


def home(request):
    """首页视图"""
    # 获取已发布的文章
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # 分页
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 推荐文章
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:5]
    
    # 热门文章（按阅读量排序）
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    # 最新文章
    latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:5]
    
    # 分类列表
    categories = Category.objects.all()
    
    # 标签云
    tags = Tag.objects.all()[:20]
    
    context = {
        'page_obj': page_obj,
        'featured_posts': featured_posts,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    """文章详情页"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # 增加阅读量
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()
    
    # 获取评论
    comments = Comment.objects.filter(
        post=post, 
        is_approved=True, 
        parent__isnull=True
    ).select_related('user').prefetch_related('replies__user')
    
    # 评论表单
    comment_form = CommentForm()
    
    # 上一篇和下一篇文章
    previous_post = post.get_previous_post()
    next_post = post.get_next_post()
    
    # 相关文章（同分类的其他文章）
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
    
    # 分页
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
    
    # 分页
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
    
    # 分页
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': posts.count() if query else 0,
    }
    return render(request, 'blog/search_results.html', context)


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
        
        # 处理回复
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
    
    return redirect('blog:post_detail', slug=post_slug)


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
    
    # 分页
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'year': year,
        'month': month,
        'page_obj': page_obj,
    }
    return render(request, 'blog/archive_month.html', context)