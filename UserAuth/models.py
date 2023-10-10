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
    hr_allowed_choices = (
        (1, "无HR资格"),
        (2, "HR资格申请中"),
        (3, "具有HR资格")
    )
    hr_allowed = models.SmallIntegerField(verbose_name="身份切换权限", choices=hr_allowed_choices, default=1)
    identity = models.SmallIntegerField(verbose_name="权限身份", choices=identity_choice, default=1)
    edu_ground = models.CharField(verbose_name="学历", max_length=12)
    school = models.CharField(verbose_name="学校", max_length=12)
    major = models.CharField(verbose_name="专业", max_length=12)
    excepting_position = models.CharField(verbose_name="意向职位", max_length=12)
    excepting_location = models.CharField(verbose_name="意向地点", max_length=12)

    def __str__(self):
        return self.username
