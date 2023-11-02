import hashlib

from django.conf import settings


def md5_encrypt(password):
    md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()
