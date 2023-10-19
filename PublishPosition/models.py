from django.db import models
from mdeditor.fields import MDTextField
from UserAuth.models import User

from PublishPosition.utils.district import district_list


# Create your models here.
class Position(models.Model):
    position_name = models.CharField(verbose_name="岗位名称", max_length=32)
    salary = models.IntegerField(verbose_name="薪资")
    summary = models.TextField(verbose_name="岗位简要", max_length=100)
    detail = MDTextField(verbose_name="详细内容", max_length=3000)
    HR = models.ForeignKey(verbose_name="联系人", to=User, to_field="id", on_delete=models.CASCADE)
    district = models.SmallIntegerField(verbose_name="所属地区", choices=district_list, default=0)
    published_choice = (
        (1, "已发布"),
        (0, "未发布"),
    )
    published_state = models.SmallIntegerField(verbose_name="岗位状态", choices=published_choice)

    def __str__(self):
        return self.position_name
