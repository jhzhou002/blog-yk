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
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket_name = settings.QINIU_BUCKET_NAME
        
        q = Auth(access_key, secret_key)
        
        file_extension = 'jpg'  # 默认扩展名，可以根据实际情况修改
        filename = f'blog-yk/{folder}/{uuid.uuid4().hex}.{file_extension}'
        
        token = q.upload_token(bucket_name, filename, 3600)
        
        ret, info = put_data(token, filename, file_data)
        
        if info.status_code == 200:
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
        
        key_prefix = f'blog-yk/{folder}/'
        
        policy = {
            'scope': bucket_name,
            'deadline': 3600,
            'insertOnly': 1,
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
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def get_client_ip(request):
    """获取客户端真实IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_slug(model_class, title, slug_field='slug'):
    """生成唯一的slug"""
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