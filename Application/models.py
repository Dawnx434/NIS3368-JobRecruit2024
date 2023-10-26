import datetime
from django.db import models

from UserAuth.models import User
from PublishPosition.models import Position


# Create your models here.
class Application(models.Model):
    applicant = models.ForeignKey(verbose_name='申请者', to=User, to_field="id", on_delete=models.CASCADE)
    position = models.ForeignKey(verbose_name='申请岗位', to=Position, to_field="id", on_delete=models.CASCADE)
    application_time = models.DateTimeField(verbose_name='最后申请时间', auto_now=False)
    create_time = models.DateTimeField(verbose_name='申请创建时间', auto_now_add=False)
    active_state_choices = (
        (1, '已申请'),
        (0, '已取消')
    )
    active_state = models.SmallIntegerField(verbose_name="申请状态", choices=active_state_choices, default=1)

    def __str__(self):
        return "{}于{}申请了{}".format(self.applicant,
                                       (self.application_time + datetime.timedelta(hours=8)).strftime(
                                           "%Y-%m-%d %H:%M:%S"),
                                       self.position)
