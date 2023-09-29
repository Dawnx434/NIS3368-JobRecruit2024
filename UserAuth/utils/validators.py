import re


def is_valid_email(email):
    # 正则表达式模式，用于匹配合法的邮箱地址
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # 使用 re 模块进行匹配
    if re.match(pattern, email):
        return True
    else:
        return False
