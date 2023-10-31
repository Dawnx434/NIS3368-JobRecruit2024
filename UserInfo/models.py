from django.db import models

from UserAuth.models import User


class Resume(models.Model):
    name = models.CharField(verbose_name="简历名称", max_length=40)
    file_path = models.CharField(verbose_name="简历路径", max_length=200)
    belong_to = models.ForeignKey(verbose_name="所属用户", to=User, to_field='id',on_delete=models.CASCADE)

    def __str__(self):
        return "{}的简历：{}".format(self.belong_to.username, self.name)
