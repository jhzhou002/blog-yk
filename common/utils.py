import os
import uuid
from django.conf import settings
from qiniu import Auth, put_data
import requests


def upload_to_qiniu(file_data, folder='images'):
    """
    上传文件到七牛云
    :param file_data: 文件数据
    :param folder: 存储文件夹
    :return: 上传后的URL或None
    """
    try:
        # 七牛云配置
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket_name = settings.QINIU_BUCKET_NAME
        
        # 认证
        q = Auth(access_key, secret_key)
        
        # 生成唯一文件名
        file_extension = 'jpg'  # 默认扩展名，可以根据实际情况修改
        filename = f'blog-yk/{folder}/{uuid.uuid4().hex}.{file_extension}'
        
        # 生成上传Token
        token = q.upload_token(bucket_name, filename, 3600)
        
        # 上传文件
        ret, info = put_data(token, filename, file_data)
        
        if info.status_code == 200:
            # 返回访问URL
            domain = settings.QINIU_DOMAIN
            return f'http://{domain}/{filename}' if domain else ret.get('key')
        else:
            return None
            
    except Exception as e:
        print(f"上传到七牛云失败: {e}")
        return None


def get_qiniu_upload_token(folder='images'):
    """
    获取七牛云上传凭证（用于前端直传）
    :param folder: 存储文件夹
    :return: 上传凭证和文件名
    """
    try:
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket_name = settings.QINIU_BUCKET_NAME
        
        q = Auth(access_key, secret_key)
        
        # 生成唯一文件名前缀
        key_prefix = f'blog-yk/{folder}/'
        
        # 上传策略
        policy = {
            'scope': bucket_name,
            'deadline': 3600,  # 1小时后过期
            'insertOnly': 1,   # 只允许新增文件
            'mimeLimit': 'image/jpeg;image/png;image/gif;image/webp'
        }
        
        token = q.upload_token(bucket_name, None, 3600, policy)
        
        return {
            'token': token,
            'key_prefix': key_prefix,
            'domain': settings.QINIU_DOMAIN
        }
        
    except Exception as e:
        print(f"获取上传凭证失败: {e}")
        return None


def truncate_text(text, max_length=100):
    """
    截断文本
    :param text: 原始文本
    :param max_length: 最大长度
    :return: 截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def get_client_ip(request):
    """
    获取客户端真实IP地址
    :param request: Django request对象
    :return: IP地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_slug(model_class, title, slug_field='slug'):
    """
    生成唯一的slug
    :param model_class: 模型类
    :param title: 标题
    :param slug_field: slug字段名
    :return: 唯一的slug
    """
    from django.utils.text import slugify
    
    base_slug = slugify(title)
    if not base_slug:
        base_slug = uuid.uuid4().hex[:8]
    
    slug = base_slug
    counter = 1
    
    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


def send_notification_email(subject, message, recipient_list):
    """
    发送通知邮件
    :param subject: 邮件主题
    :param message: 邮件内容
    :param recipient_list: 收件人列表
    :return: 发送结果
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False


def cache_key_generator(*args):
    """
    生成缓存键
    :param args: 参数列表
    :return: 缓存键
    """
    return ':'.join(str(arg) for arg in args)


class PaginationMixin:
    """分页混合类"""
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', self.paginate_by)