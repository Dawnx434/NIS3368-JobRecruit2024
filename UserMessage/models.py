from django.db import models

from UserAuth.models import User


# Create your models here.
class Message(models.Model):
    from_user = models.ForeignKey(verbose_name="发送者", to=User, to_field='id', on_delete=models.CASCADE,
                                  related_name="Message_from_user")
    to_user = models.ForeignKey(verbose_name="接收方", to=User, to_field='id', on_delete=models.CASCADE,
                                related_name="Message_to_user")
    title = models.CharField(verbose_name="标题", max_length=32)
    content = models.TextField(verbose_name="内容", max_length=2000)
    create_time = models.DateTimeField(verbose_name='私信发送时间', auto_now_add=False)
