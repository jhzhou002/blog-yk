from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from .models import Comment


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