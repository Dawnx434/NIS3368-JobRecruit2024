from django.test import TestCase

from UserAuth.utils.validators import is_valid_email


# Create your tests here.
class UserAuthTests(TestCase):
    """
    下述测试测试邮箱校验函数是否正确
    """
    def test_email_validator_with_real_email(self):
        real_email = 'felix_chen@sjtu.edu.cn'
        self.assertIs(is_valid_email(real_email), True)

    def test_email_validator_with_fake_email(self):
        fake_email = 'felix_chen.sjtu.edu.cn'
        self.assertIs(is_valid_email(fake_email), False)
