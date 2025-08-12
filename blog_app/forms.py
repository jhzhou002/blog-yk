from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column
from .models import Comment, Profile, Post, Category, Tag, SiteSettings


# ==================== 评论表单 ====================

class CommentForm(forms.ModelForm):
    """评论表单"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入您的评论...'
            }),
        }
        labels = {
            'content': '评论内容',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('content', css_class='mb-3'),
            Div(
                Submit('submit', '发表评论', css_class='btn btn-primary'),
                css_class='d-grid gap-2'
            )
        )


class SearchForm(forms.Form):
    """搜索表单"""
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '搜索文章...',
            'autocomplete': 'off'
        }),
        label='',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'd-flex'
        self.helper.layout = Layout(
            Div(
                Field('q', css_class='me-2 flex-grow-1'),
                Submit('submit', '搜索', css_class='btn btn-outline-primary'),
                css_class='d-flex'
            )
        )


# ==================== 用户认证表单 ====================

class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    email = forms.EmailField(required=True, label='邮箱')
    first_name = forms.CharField(max_length=30, required=False, label='姓')
    last_name = forms.CharField(max_length=30, required=False, label='名')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Row(
                Column(Field('first_name', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('last_name', css_class='mb-3'), css_class='col-md-6'),
            ),
            Field('email', css_class='mb-3'),
            Field('password1', css_class='mb-3'),
            Field('password2', css_class='mb-3'),
            Div(
                Submit('submit', '注册', css_class='btn btn-primary w-100'),
                css_class='d-grid'
            )
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    """自定义登录表单"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        label='用户名'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        label='密码'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='记住我'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Field('password', css_class='mb-3'),
            Div(
                Field('remember_me', css_class='form-check'),
                css_class='mb-3'
            ),
            Div(
                Submit('submit', '登录', css_class='btn btn-primary w-100'),
                css_class='d-grid'
            )
        )


class UserUpdateForm(forms.ModelForm):
    """用户信息更新表单"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('last_name', css_class='mb-3'), css_class='col-md-6'),
            ),
            Field('email', css_class='mb-3'),
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
    """用户资料更新表单"""
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'website', 'github', 'location', 'birth_date', 'phone')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('avatar', css_class='mb-3'),
            Field('bio', css_class='mb-3'),
            Row(
                Column(Field('website', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('github', css_class='mb-3'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('location', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('phone', css_class='mb-3'), css_class='col-md-6'),
            ),
            Field('birth_date', css_class='mb-3'),
            Div(
                Submit('submit', '更新资料', css_class='btn btn-primary'),
                css_class='d-grid gap-2'
            )
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# ==================== 管理表单 ====================

class PostForm(forms.ModelForm):
    """文章表单"""
    
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'tags', 'content', 'excerpt', 
                 'cover_image', 'status', 'is_featured']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(Field('title', css_class='mb-3'), css_class='col-md-8'),
                Column(Field('slug', css_class='mb-3'), css_class='col-md-4'),
            ),
            Row(
                Column(Field('category', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('status', css_class='mb-3'), css_class='col-md-6'),
            ),
            Field('tags', css_class='mb-3'),
            Field('content', css_class='mb-3'),
            Field('excerpt', css_class='mb-3'),
            Field('cover_image', css_class='mb-3'),
            Row(
                Column(
                    Field('is_featured', css_class='form-check-input'), 
                    css_class='col-md-6'
                ),
            ),
            Div(
                Submit('submit', '保存文章', css_class='btn btn-primary me-2'),
                css_class='d-flex gap-2'
            )
        )
        
        for field in self.fields.values():
            if field.widget.__class__.__name__ not in ['CheckboxSelectMultiple', 'CheckboxInput']:
                field.widget.attrs.update({'class': 'form-control'})


class CategoryForm(forms.ModelForm):
    """分类表单"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('slug', css_class='mb-3'),
            Field('description', css_class='mb-3'),
            Div(
                Submit('submit', '保存分类', css_class='btn btn-primary'),
                css_class='d-grid gap-2'
            )
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TagForm(forms.ModelForm):
    """标签表单"""
    
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(Field('name', css_class='mb-3'), css_class='col-md-6'),
                Column(Field('slug', css_class='mb-3'), css_class='col-md-6'),
            ),
            Field('color', css_class='mb-3'),
            Div(
                Submit('submit', '保存标签', css_class='btn btn-primary'),
                css_class='d-grid gap-2'
            )
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['color'].widget.attrs.update({'type': 'color'})


class SiteSettingsForm(forms.ModelForm):
    """网站设置表单"""
    
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'site_description', 'site_keywords', 'site_author',
                 'site_logo', 'favicon', 'footer_text', 'github_url', 'weibo_url',
                 'wechat_qr', 'google_analytics', 'baidu_statistics',
                 'comment_moderation', 'allow_anonymous_comments']
        widgets = {
            'site_description': forms.Textarea(attrs={'rows': 3}),
            'footer_text': forms.Textarea(attrs={'rows': 3}),
            'google_analytics': forms.Textarea(attrs={'rows': 4}),
            'baidu_statistics': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Submit('submit', '保存设置', css_class='btn btn-primary')
        )
        
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})