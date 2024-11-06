import re


import re

def is_valid_email(email):
    # 检查 email 是否为 None 或空字符串，避免传入 None 引发错误
    if not email:
        return False

    # 正则表达式模式，用于匹配合法的邮箱地址
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # 使用 re.match 进行匹配，直接返回匹配结果
    return re.match(pattern, email) is not None



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
