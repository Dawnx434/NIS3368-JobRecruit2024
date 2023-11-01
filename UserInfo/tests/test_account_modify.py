from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail

from UserAuth.models import User
from UserInfo.views import account

from Forum.models import Topic, Post


class InfoResumeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                   email='songyhinf@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        url = reverse('UserInfo:account')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_url_resolve_index_view(self):
        view = resolve('/info/account/')
        self.assertEqual(view.func, account)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        self.assertContains(self.response, '<form')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 11)
        self.assertContains(self.response, 'type="text"', 5)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulModifyTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                        email='songyhinf@qq.com',
                                        gender=1, hr_allowed=1, identity=1, school='SJTU')
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)

        url = reverse('UserAuth:sendemail')
        self.response = self.client.post(url, {'email_address': 'songyhinf@qq.com'})
        code = mail.outbox[0].body[9:15]
        data = {
            'username': 'songyunhao',
            'password': '0123456789',
            'confirm_password': '0123456789',
            'mobile_phone': '17325493149',
            'email': 'songyhinf@qq.com',
            'verification_code': code
        }
        self.success_response = self.client.post(reverse('UserInfo:account'), data)

    def test_valid_modify(self):
        self.assertEqual(self.success_response.status_code, 200)
