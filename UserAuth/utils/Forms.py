from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from UserAuth import models
from UserAuth.utils.bootstrapform import BootStrapForm
from UserAuth.utils.validators import is_username_valid
from UserAuth.utils.encrypt import verify_encrypted_password
import re
import os
from django.conf import settings

class RegisterForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=350,
        widget=forms.PasswordInput(attrs={'placeholder': "请输入密码"}, render_value=True)
    )
    check_password = forms.CharField(
        label="确认密码",
        max_length=350,
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
            raise ValidationError("手机号已存在")
        return self.cleaned_data['mobile_phone']

    def clean_email(self):
        if models.User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError("邮箱已存在")
        return self.cleaned_data['email']

    def clean_verification_code(self):
        code_in_session = self.request.session.get('register_verification_code')
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'].upper() == code_in_session.upper():
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']

    # def clean_check_password(self):
    #     password = self.cleaned_data.get('password')
    #     check_password = self.cleaned_data.get('check_password')
    #     if password and check_password and password != check_password:
    #         raise ValidationError("两次输入的密码不一致！")
    #     return check_password
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #
    #     # 检查密码长度
    #     if len(password) < 8:
    #         raise ValidationError("密码长度必须至少为8位。")
    #     if self.cleaned_data['username'].lower() in password.lower():
    #         raise ValidationError("密码不能与用户名过于相似。")
    #     # 检查常见密码
    #     common_passwords_path = os.path.join(settings.BASE_DIR, 'common_passwords.txt')
    #     try:
    #         with open(common_passwords_path, 'r', encoding='utf-8') as f:
    #             common_passwords = f.read().splitlines()
    #         if password in common_passwords:
    #             raise ValidationError("此密码过于常见，请选择其他密码。")
    #     except FileNotFoundError:
    #         raise ValidationError("常见密码字典文件未找到，请联系管理员。")
    #     # 检查密码复杂度
    #     if not re.search(r'[A-Z]', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少大写字母。")
    #     if not re.search(r'[a-z]', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少小写字母。")
    #     if not re.search(r'\d', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少数字。")
    #
    #     return password


class LoginForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label="密码",
        max_length=350,
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
        if row_obj and verify_encrypted_password((self.cleaned_data['password']), row_obj.password):
            return ''
        else:
            raise ValidationError("用户名或密码错误")

    def clean_verification_code(self):
        code_in_session = self.request.session.get('login_verification_code')
        if not code_in_session:
            raise ValidationError("验证码已过期")
        # 将用户输入的验证码转换为小写进行比较
        if not self.cleaned_data['verification_code'].lower() == code_in_session.lower():
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']


class ResetPasswordForm(BootStrapForm, forms.Form):
    username_or_mobile = forms.CharField(
        label="手机号或用户名",
        max_length=64,
    )
    password = forms.CharField(
        label="新密码",
        max_length=350,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}, render_value=True)
    )
    check_password = forms.CharField(
        label="确认新密码",
        max_length=350,
        widget=forms.PasswordInput(attrs={'placeholder': '请确认新密码'}, render_value=True)
    )
    verification_code = forms.CharField(
        label="邮箱验证码",
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

    # def clean_check_password(self):
    #     password = self.cleaned_data.get('password')
    #     check_password = self.cleaned_data.get('check_password')
    #     if password and check_password and password != check_password:
    #         raise ValidationError("两次输入的密码不一致！")
    #     return check_password
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #
    #     # 检查密码长度
    #     if len(password) < 8:
    #         raise ValidationError("密码长度必须至少为8位。")
    #     if self.cleaned_data['username_or_mobile'].lower() in password.lower():
    #         raise ValidationError("密码不能与用户名或手机号过于相似。")
    #     # 检查常见密码
    #     common_passwords_path = os.path.join(settings.BASE_DIR, 'common_passwords.txt')
    #     try:
    #         with open(common_passwords_path, 'r', encoding='utf-8') as f:
    #             common_passwords = f.read().splitlines()
    #         if password in common_passwords:
    #             raise ValidationError("此密码过于常见，请选择其他密码。")
    #     except FileNotFoundError:
    #         raise ValidationError("常见密码字典文件未找到，请联系管理员。")
    #     # 检查密码复杂度
    #     if not re.search(r'[A-Z]', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少大写字母。")
    #     if not re.search(r'[a-z]', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少小写字母。")
    #     if not re.search(r'\d', password):
    #         raise ValidationError("密码必须包含至少一个大写字母、一个小写字母、一个数字。缺少数字。")
    #
    #     return password