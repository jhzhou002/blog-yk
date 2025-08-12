from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """用户扩展资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.URLField('头像URL', blank=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)
    website = models.URLField('个人网站', blank=True)
    github = models.CharField('GitHub', max_length=100, blank=True)
    location = models.CharField('所在地', max_length=100, blank=True)
    birth_date = models.DateField('生日', null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} 的资料'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """用户保存时保存Profile"""
    if hasattr(instance, 'profile'):
        instance.profile.save()