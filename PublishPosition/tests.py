from django.test import TestCase

from PublishPosition.utils.check_html_keywords import dont_contain_html_keywords


# Create your tests here.
class CheckHtmlReservedWords(TestCase):
    def test_check_html_keywords_case_1(self):
        valid_input = "<script>alert('XSS')</script>"
        self.assertIs(dont_contain_html_keywords(valid_input), False)

    def test_check_html_keywords_case_2(self):
        valid_input = "alert('XSS')"
        self.assertIs(dont_contain_html_keywords(valid_input), True)
