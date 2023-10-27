from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.utils.Forms import RegisterForm
from UserAuth.utils.validators import is_valid_email, is_username_valid
from UserAuth.views import register
from UserAuth.models import User
from django.core import mail


# Create your tests here.
class UserAuthTests(TestCase):
    """
    下述测试测试邮箱校验函数是否正确
    """

    def test_email_validator_with_real_email(self):
        real_email = 'felix_chen@sjtu.edu.cn'
        self.assertIs(is_valid_email(real_email), True)

    def test_email_validator_with_fake_email(self):
        fake_email = 'felix_chen.sjtu.edu.cn'
        self.assertIs(is_valid_email(fake_email), False)

    def test_email_validator_with_fake_email_2(self):
        fake_email = '0'
        self.assertIs(is_valid_email(fake_email), False)

    def test_username_validator_with_valid_username(self):
        valid_username = 'Felix_Chen'
        self.assertIs(is_username_valid(valid_username), True)

    def test_username_validator_with_invalid_username(self):
        invalid_username = "Felix Chen"
        self.assertIs(is_username_valid(invalid_username), False)


class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('UserAuth:register')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/auth/register/')
        self.assertEquals(view.func, register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterForm)

    def test_form_inputs(self):
        """
        注册表单含有 8 inputs: csrf, username, 'password', 'check_password', 'gender', 'mobile_phone', 'email', 'verification_code'
        """
        self.assertContains(self.response, '<input', 8)
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignupTests(TestCase):

    def setUp(self):

        url = reverse('UserAuth:sendemail')
        self.response = self.client.post(url, {'email_address': 'songyhinf@qq.com'})
        code = mail.outbox[0].body[9:15]
        url_register = reverse('UserAuth:register')
        data = {
            'username': 'john',
            'password': '0123456789',
            'check_password': '0123456789',
            'gender': 1,
            'mobile_phone': '17325493149',
            'email': 'songyhinf@qq.com',
            'verification_code': code,
        }
        self.response_register = self.client.post(url_register, data)

    def test_send_verification_code(self):
        """
        测试邮箱验证码是否被正确发送
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_code(self):
        """
        测试能否正常注册
        """
        self.assertEqual(self.response_register.status_code, 302)

    def test_redirection(self):
        """
        测试能否正常重定向到首页
        """
        self.assertEqual(self.response_register['Location'], '/')

    def test_user_creation(self):
        """
        测试用户有没有正常创建
        """
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        测试进入主页后用户有没有被放在会话中
        """
        response = self.client.get(reverse('Forum:home'))
        UserInfo = self.client.session['UserInfo']
        self.assertEqual(UserInfo.get('username'), 'john')


class InvalidSignUpTests(TestCase):
    def setUp(self):
        """
        提交空表单
        """
        url = reverse('UserAuth:register')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """
        不合法提交应该返回当前页面
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        """
        应无用户
        """
        self.assertFalse(User.objects.exists())
