from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from UserAuth import models
from UserAuth.utils.bootstrapform import BootStrapForm

from UserAuth.utils.validators import is_username_valid


class RegisterForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': "请输入密码"}, render_value=True)
    )
    check_password = forms.CharField(
        label="确认密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}, render_value=True)
    )
    mobile_phone = forms.CharField(
        label="手机号",
        max_length=32,
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')]
    )
    email = forms.CharField(
        label="邮箱",
        max_length=32,
        validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', '邮箱格式错误')]
    )
    verification_code = forms.CharField(
        label="验证码",
        max_length=10
    )

    class Meta:
        model = models.User
        fields = ['username', 'password', 'check_password', 'gender', 'mobile_phone', 'email', 'verification_code']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        if not is_username_valid(self.cleaned_data['username']):
            raise ValidationError("用户名不允许存在特殊字符")
        if models.User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise ValidationError("用户名已存在")
        return self.cleaned_data['username']

    def clean_mobile_phone(self):
        if models.User.objects.filter(mobile_phone=self.cleaned_data['mobile_phone']).exists():
            raise ValidationError("邮箱已存在")
        return self.cleaned_data['mobile_phone']

    def clean_email(self):
        if models.User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError("邮箱已存在")
        return self.cleaned_data['email']

    def clean_check_password(self):
        if not self.cleaned_data['password'] == self.cleaned_data['check_password']:
            raise ValidationError("两次密码不一致")
        return self.cleaned_data['check_password']

    def clean_verification_code(self):
        code_in_session = self.request.session['verification_code']
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']


class LoginForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=64,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}, render_value=True)
    )
    verification_code = forms.CharField(
        label="图形验证码",
        max_length=32
    )

    class Meta:
        model = models.User
        fields = ['username']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        row_obj = models.User.objects.filter(username=self.cleaned_data.get('username')).first()
        if row_obj and row_obj.password == self.cleaned_data['password']:
            return self.cleaned_data['password']
        else:
            raise ValidationError("用户名或密码错误")

    def clean_verification_code(self):
        code_in_session = self.request.session.get('verification_code')
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']


class ResetPasswordForm(BootStrapForm, forms.Form):
    username_or_mobile = forms.CharField(
        label="手机号或用户名",
        max_length=64,
    )
    verification_code = forms.CharField(
        label="验证码",
        max_length=32
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_verification_code(self):
        code_in_session = self.request.session.get('reset_password_verification_code')
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']
