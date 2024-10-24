from django.db import models
from mdeditor.fields import MDTextField
from UserAuth.models import User
from PublishPosition.utils.district import district_list

# Create your models here.
class Position(models.Model):
    position_name = models.CharField(verbose_name="岗位名称", max_length=32)
    salary_min = models.IntegerField(verbose_name="最低薪资", default=0)  # 新增字段：最低薪资
    salary_max = models.IntegerField(verbose_name="最高薪资", default=0)  # 新增字段：最高薪资
    salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)  # 原salary定义为平均薪资
    def save(self, *args, **kwargs):
        # 计算 salary 字段的值
        if self.salary_min is not None and self.salary_max is not None:
            self.salary = (int(self.salary_min) + int(self.salary_max)) / 2
        else:
            self.salary = None  # 或者你可以设置为0或者其他默认值

        super().save(*args, **kwargs)  # 调用父类的 save 方法
    summary = models.TextField(verbose_name="岗位简要", max_length=100)
    detail = MDTextField(verbose_name="详细内容", max_length=3000)
    HR = models.ForeignKey(verbose_name="联系人", related_name='positions', to=User, to_field="id", on_delete=models.CASCADE)
    district = models.SmallIntegerField(verbose_name="所属地区", choices=district_list, default=None)
    job_type = models.CharField(verbose_name="岗位类型", max_length=20, default="")  # 新增字段：岗位类型
    education_requirements = models.CharField(verbose_name="学历要求", max_length=20, default="")  # 新增字段：学历要求
    published_choice = (
        (1, "已发布"),
        (0, "未发布"),
    )
    published_state = models.SmallIntegerField(verbose_name="岗位状态", choices=published_choice)

    def __str__(self):
        return self.position_name
