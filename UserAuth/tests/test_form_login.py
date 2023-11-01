from django.test import TestCase
from UserAuth.utils.Forms import LoginForm


class LoginFormTest(TestCase):

    def test_login_form_has_fields(self):
        form = LoginForm(request=None)
        expected = ['username', 'password', 'verification_code']
        actual = list(form.fields)
        # print(actual)
        self.assertSequenceEqual(expected, actual)
