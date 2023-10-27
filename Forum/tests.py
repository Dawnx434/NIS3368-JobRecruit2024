from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User


# Create your tests here.
class HomeTests(TestCase):

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
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': username,
            'password': password,
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        url = reverse('Forum:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

