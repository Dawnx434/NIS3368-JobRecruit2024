from django.db import models


# Create your models here.
class User(models.Model):
    """用户信息"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    mobile_phone = models.CharField(verbose_name="手机号", max_length=32)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    gender_choice = (
        (1, "不愿透露"),
        (2, "男"),
        (3, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, default=1)
    identity_choice = (
        (1, "用户"),
        (2, "HR"),
        (3, "管理员")
    )
    identity = models.SmallIntegerField(verbose_name="权限身份", choices=identity_choice, default=1)

    def __str__(self):
        return self.username
