from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column
from blog.models import Post, Category, Tag
from common.models import SiteSettings


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
        
        # 设置字段属性
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
        
        # 颜色选择器
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
            Div(
                'site_name', 'site_author', 'site_description', 'site_keywords',
                css_class='card-body',
                style='border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;'
            ),
            Div(
                'site_logo', 'favicon', 'footer_text',
                css_class='card-body',
                style='border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;'
            ),
            Div(
                'github_url', 'weibo_url', 'wechat_qr',
                css_class='card-body',
                style='border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;'
            ),
            Div(
                'google_analytics', 'baidu_statistics',
                css_class='card-body',
                style='border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;'
            ),
            Div(
                'comment_moderation', 'allow_anonymous_comments',
                css_class='card-body',
                style='border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;'
            ),
            Submit('submit', '保存设置', css_class='btn btn-primary')
        )
        
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})