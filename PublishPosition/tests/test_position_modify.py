from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User

from PublishPosition.views import modify_position
from PublishPosition.models import Position


class ModifyPositionTest(TestCase):

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
        self.position = Position.objects.create(position_name='sss', salary=1000, summary='dwad', detail='dwad',
                                                HR=self.user, district=0, published_state=0)
        url = reverse('PublishPosition:modify_position', kwargs={'nid': self.position.pk})
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_url_resolve_index_view(self):
        view = resolve('/position/modify/1/')
        self.assertEqual(view.func, modify_position)

    def test_contain_home_url(self):
        home_url = reverse('Forum:home')
        self.assertContains(self.response, f'href="{home_url}"')

    def test_contain_publish_position_url(self):
        publish_position_url = reverse('PublishPosition:publish')
        self.assertContains(self.response, f'href="{publish_position_url}"')

    def test_contain_add_new_topic_url(self):
        new_topic_url = reverse('Forum:new_topic')
        self.assertContains(self.response, f'href="{new_topic_url}"')

    def test_contain_form(self):
        self.assertContains(self.response, '<form')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="text"', 1)


class SuccessfulModifyTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                        email='songyhinf@qq.com',
                                        gender=1, hr_allowed=2, identity=3, school='SJTU')
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)

        self.position = Position.objects.create(position_name='sss', salary=1000, summary='dwad', detail='dwad',
                                                HR=self.user, district=0, published_state=0)
        url = reverse('PublishPosition:modify_position', kwargs={'nid': self.position.pk})

        data = {
            'position_name': 'sss',
            'salary': 2000,
            'summary': 'dwad',
            'detail': 'dawd',
            'district': 0,
            'published_state': 0,
        }
        self.success_response = self.client.post(url, data)

    def test_valid_modify(self):
        self.assertEqual(self.success_response.status_code, 200)

    # def test_success_publish(self):
    #     self.assertEqual(self.position.salary, 2000)

