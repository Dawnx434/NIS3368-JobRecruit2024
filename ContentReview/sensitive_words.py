import re

# 定义一个函数来从文件加载敏感词列表
def load_sensitive_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()
    return words

# 在需要使用的地方加载敏感词
SENSITIVE_WORDS = load_sensitive_words('ContentReview/sensitive_words.txt')

def censor_content(content):
    """
    审查内容，替换敏感词为**
    :param content: 用户提交的内容
    :return: 审查后的内容
    """
    for word in SENSITIVE_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        content = pattern.sub('**', content)
    return content