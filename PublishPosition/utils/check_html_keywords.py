import re


def dont_contain_html_keywords(input_string):
    pattern = r'<.*?>'
    matched = re.search(pattern, input_string)
    return not matched
