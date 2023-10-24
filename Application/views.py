from django.shortcuts import render, HttpResponse
from django.utils import timezone

from PublishPosition.models import Position
from UserAuth.models import User
from Application.models import Application


# Create your views here.
def apply(request, pid):
    """申请职位视图"""
    # 获取职位和用户对象
    position_query_set = Position.objects.filter(id=pid)
    user_query_set = User.objects.filter(id=request.session.get("UserInfo").get("id"))
    # 检查空值
    if not position_query_set:
        return HttpResponse("不合法的岗位")
    if not user_query_set:
        return HttpResponse("无效的用户信息")
    # 选择对象
    position_obj = position_query_set.first()
    user_obj = user_query_set.first()
    # 检查岗位是否开放
    if not position_obj.published_state == 1:
        return HttpResponse("未开放的岗位")
    # 检查是否未申请过
    application_query_set = Application.objects.filter(applicant=user_obj, position=position_obj)
    # 没有记录
    if not application_query_set:
        # 则写入新记录
        Application.objects.create(**{
            'applicant': user_obj,
            'position': position_obj,
            'application_time': timezone.localtime(),
            'create_time': timezone.localtime()
        })
        return HttpResponse("申请成功")

    # 如果有记录
    application_obj = application_query_set.first()
    if application_obj.active_state == 0:
        # 未生效则使之生效
        application_query_set.update(**{
            'application_time': timezone.localtime(),
            'active_state': 1,
        })

    # 已生效则无需更改
    return HttpResponse("已申请过该职位！")


def cancel(request, pid):
    """取消职位视图"""
    # 获取职位和用户对象
    position_query_set = Position.objects.filter(id=pid)
    user_query_set = User.objects.filter(id=request.session.get("UserInfo").get("id"))
    # 检查空值
    if not position_query_set:
        return HttpResponse("不合法的岗位")
    if not user_query_set:
        return HttpResponse("无效的用户信息")
    # 选择对象
    position_obj = position_query_set.first()
    user_obj = user_query_set.first()
    # 检查岗位是否开放
    if not position_obj.published_state == 1:
        return HttpResponse("未开放的岗位")
    # 检查是否已经申请过
    application_query_set = Application.objects.filter(applicant=user_obj, position=position_obj)
    if not application_query_set:
        return HttpResponse("不存在申请记录！")
    # 通过检查
    data_dict = {
        'application_time': timezone.localtime(),
        'active_state': 0
    }
    application_query_set.update(**data_dict)
    return HttpResponse("取消申请成功")
