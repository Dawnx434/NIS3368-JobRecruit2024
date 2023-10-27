from django.test import TestCase
from UserAuth.utils.Forms import RegisterForm


class SignUpFormTest(TestCase):

    def test_form_has_fields(self):
        form = RegisterForm(request=None)
        expected = ['username', 'password', 'check_password', 'gender', 'mobile_phone', 'email', 'verification_code',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
