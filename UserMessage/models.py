import datetime

from django.db import models

from UserAuth.models import User


# Create your models here.
class Message(models.Model):
    from_user = models.ForeignKey(verbose_name="发送者", to=User, to_field='id', on_delete=models.CASCADE,
                                  related_name="Message_from_user")
    to_user = models.ForeignKey(verbose_name="接收方", to=User, to_field='id', on_delete=models.CASCADE,
                                related_name="Message_to_user")
    title = models.CharField(verbose_name="标题", max_length=100)
    content = models.TextField(verbose_name="内容", max_length=2000)
    create_time = models.DateTimeField(verbose_name='私信发送时间', auto_now_add=False)
    read_choice = (
        (0, "未读"),
        (1, "已读")
    )
    read = models.SmallIntegerField(verbose_name="私信状态", choices=read_choice, default=0)
    reply_to = models.ForeignKey(verbose_name="回复至", to='self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}于{}发往{}的私信".format(self.from_user, (self.create_time + datetime.timedelta(hours=8)).strftime(
            "%Y-%m-%d %H:%M:%S"), self.to_user)
