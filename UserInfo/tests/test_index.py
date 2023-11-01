from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User
from UserInfo.views import index

from Forum.models import Topic, Post


class InfoIndexTest(TestCase):

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
        self.topic = Topic.objects.create(subject='hello', starter=self.user)
        url = reverse('UserInfo:index', kwargs={'pk': self.user.pk})
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_url_resolve_index_view(self):
        view = resolve('/info/index/1/')
        self.assertEqual(view.func, index)

    def test_contain_home_url(self):
        home_url = reverse('Forum:home')
        self.assertContains(self.response, f'href="{home_url}"')

    def test_contain_publish_position_url(self):
        publish_position_url = reverse('PublishPosition:publish')
        self.assertContains(self.response, f'href="{publish_position_url}"')

    def test_contain_add_new_topic_url(self):
        new_topic_url = reverse('Forum:new_topic')
        self.assertContains(self.response, f'href="{new_topic_url}"')

    def test_contain_added_topic(self):
        url = reverse('Forum:topic_posts', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, f'href="{url}"')
