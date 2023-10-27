from django.test import TestCase
from django.urls import reverse, resolve

from Forum.models import Topic, Post
from Forum.views import reply_topic
from Forum.forms import PostForm

from UserAuth.models import User


class ReplyTopicTestCase(TestCase):
    """
    Base test case
    """
    def setUp(self):
        user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                   email='songyhinf@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.topic = Topic.objects.create(subject='Hello', starter=user)
        Post.objects.create(message='HHHHHH', topic=self.topic, created_by=user)
        self.url = reverse('Forum:reply', kwargs={'pk': self.topic.pk})


class LoginRequireReplyTopicTests(ReplyTopicTestCase):

    def test_redirect_to_home(self):
        url = reverse('UserAuth:login')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, url)


class ReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/topics/1/reply/')
        self.assertEqual(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.response = self.client.post(self.url, {'message': 'Hello'})

    def test_redirection(self):
        topic_posts_url = reverse('Forum:topic_posts', kwargs={'pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)