from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User

from Forum.models import Topic, Post
from Forum.views import home, topic_posts


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
        user = User.objects.create(username=username, password=password, mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': username,
            'password': password,
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)

        self.topic = Topic.objects.create(subject='Hello', starter=user)
        Post.objects.create(message='HHHHHH', topic=self.topic, created_by=user)

        url = reverse('Forum:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        topic_posts_url = reverse('Forum:topic_posts', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, 'href="{0}"'.format(topic_posts_url))


class LoginRequireTests(TestCase):

    def setUp(self):
        self.url = reverse('Forum:home')
        self.response = self.client.get(self.url, follow=True)

    def test_redirect_to_login(self):
        login_url = reverse('UserAuth:login')
        self.assertRedirects(self.response, login_url)


class TopicPostsTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                   email='songyhinf@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.topic = Topic.objects.create(subject='Hello', starter=user)
        Post.objects.create(message='HHHHHH', topic=self.topic, created_by=user)

    def test_topic_posts_view_success_status_code(self):
        url = reverse('Forum:topic_posts', kwargs={'pk': self.topic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_posts_view_not_found_status_code(self):
        url = reverse('Forum:topic_posts', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_posts_url_resolves_topic_posts_view(self):
        view = resolve(f'/topics/{self.topic.pk}/')
        self.assertEqual(view.func, topic_posts)

