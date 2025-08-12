from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column
from .models import Profile


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
        
        # 自定义字段属性
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