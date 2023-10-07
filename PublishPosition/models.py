from django.db import models
from UserAuth.models import User


# Create your models here.
class Position(models.Model):
    position_name = models.CharField(verbose_name="岗位名称", max_length=32)
    salary = models.IntegerField(verbose_name="薪资", max_length=8)
    summary = models.TextField(verbose_name="岗位简要", max_length=100)
    detail = models.TextField(verbose_name="详细内容", max_length=3000)
    HR = models.ForeignKey(verbose_name="联系人", to="User", to_field="id", on_delete=models.CASCADE)
    province = models.SmallIntegerField(verbose_name="所属省份", choices=province_list)

    def __str__(self):
        return self.position_name
