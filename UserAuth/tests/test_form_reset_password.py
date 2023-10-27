from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.utils.Forms import ResetPasswordForm


class ResetFormTest(TestCase):

    def test_reset_form_has_fields(self):
        form = ResetPasswordForm(request=None)
        expected = ['username_or_mobile', 'password', 'check_password', 'verification_code']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
