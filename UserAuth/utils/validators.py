import re


def is_valid_email(email):
    # 正则表达式模式，用于匹配合法的邮箱地址
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # 使用 re 模块进行匹配
    if re.match(pattern, email):
        return True
    else:
        return False


def is_username_valid(username):
    pattern = r'^[a-zA-Z0-9_]+$'

    # 使用正则表达式进行匹配
    if re.match(pattern, username):
        return True  # 字符串仅包含数字、字母和下划线
    else:
        return False  # 字符串包含其他字符


def is_mobile_phone_valid(mobile_phone):
    pattern = r'^(1[3456789]\d{9})$'

    if re.match(pattern, mobile_phone):
        return True
    else:
        return False
