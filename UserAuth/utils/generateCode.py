import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.mail import send_mail
from django.conf import settings

from UserAuth.utils.validators import is_valid_email


def check_code(width=120, height=30, char_length=5, font_file='Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, float(h)], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


def send_sms_code(target_email):
    """
    发送邮箱验证码
    :param target_email: 发到这个邮箱
    :return:
        send_status: 0 成功 -1 失败
        sms_code: 验证码
    """
    # 验证邮箱地址是否正确
    if not is_valid_email(target_email):
        return -1
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(0, 999999)
    email_from = settings.EMAIL_FROM  # 邮箱来自
    email_title = settings.EMAIL_TITLE
    email_body = "您的邮箱验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title, email_body, email_from, [target_email])
    return send_status, str(sms_code)
