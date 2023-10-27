from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User

from Forum.models import Topic, Post
from Forum.views import home, new_topic
from Forum.forms import NewTopicForm


class NewTopicTestCase(TestCase):
    """
    Base test case
    """
    def setUp(self):
        user = User.objects.create(username='songyhinf', password='0123456789', mobile_phone='17325493149',
                                   email='songyhinf@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.url = reverse('Forum:new_topic')


class LoginRequireReplyTopicTests(NewTopicTestCase):

    def test_redirect_to_home(self):
        url = reverse('UserAuth:login')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, url)


class ReplyTopicTests(NewTopicTestCase):

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
        view = resolve('/new_topic/')
        self.assertEqual(view.func, new_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(NewTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'songyhinf',
            'password': '0123456789',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.response = self.client.post(self.url, {'subject': 'hello', 'message': 'Hello'})

    def test_redirection(self):
        topic_posts_url = reverse('Forum:topic_posts', kwargs={'pk': Topic.objects.first().pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        self.assertEquals(Topic.objects.count(), 1)


class InvalidReplyTopicTests(NewTopicTestCase):

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
