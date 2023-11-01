from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail

from UserAuth.views import reset_password, reset_password_email
from UserAuth.utils.Forms import ResetPasswordForm
from UserAuth.models import User


class ResetTest(TestCase):

    def setUp(self):
        url = reverse('UserAuth:reset_password')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/auth/reset/')
        self.assertEquals(view.func, reset_password)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ResetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="password"', 2)


class ValidResetTest(TestCase):

    def setUp(self):
        username = 'songyhinf'
        password = '0123456789'
        mobile_phone = '17325493149'
        email = 'songyhinf@qq.com'
        gender = 1
        hr_allowed = 1
        identity = 1
        User.objects.create(username=username, password=password, mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        self.url = reverse('UserAuth:reset_password')

        self.mail_response = self.client.post(reverse('UserAuth:reset_password_email'), {'username_or_mobile': 'songyhinf'})
        code = mail.outbox[0].body[9:15]

        data = {
            'username_or_mobile': username,
            'password': '88888888',
            'check_password': '88888888',
            'verification_code': code,
        }

        self.valid_response = self.client.post(self.url, data)

    def test_send_verification_code(self):
        self.assertEqual(self.mail_response.status_code, 200)

    def test_valid_reset(self):
        self.assertEqual(self.valid_response.status_code, 200)

    def test_new_password(self):
        """
        测试密码有没有被修改
        """
        self.assertEqual(User.objects.first().password, '88888888')


class InvalidResetTest(TestCase):

    def setUp(self):
        username = 'songyhinf'
        password = '0123456789'
        mobile_phone = '17325493149'
        email = 'songyhinf@qq.com'
        gender = 1
        hr_allowed = 1
        identity = 1
        User.objects.create(username=username, password=password, mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        self.url = reverse('UserAuth:reset_password')

        self.mail_response = self.client.post(reverse('UserAuth:reset_password_email'),
                                              {'username_or_mobile': 'songyhinf'})
        code = mail.outbox[0].body[9:15]

        data = {
            'username_or_mobile': username,
            'password': '88888888',
            'check_password': '88888888',
            'verification_code': 'AAAAA',
        }

        self.invalid_response = self.client.post(self.url, data)
        self.blank_response = self.client.post(self.url, {})

    def test_invalid_verification_code(self):
        self.assertEqual(self.invalid_response.status_code, 200)

    def test_blank_post_form_errors(self):
        form = self.blank_response.context.get('form')
        self.assertTrue(form.errors)

    def test_password_no_change(self):
        self.assertEqual(User.objects.first().password, '0123456789')

