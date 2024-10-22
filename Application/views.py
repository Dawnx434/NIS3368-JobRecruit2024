import os
import urllib

from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.conf import settings

from PublishPosition.models import Position
from UserAuth.models import User
from Application.models import Application
from UserInfo.models import Resume


from django.shortcuts import redirect
from django.contrib import messages

def apply_all(request):
    if request.method == 'POST':
        # 获取隐藏表单中提交的 position_ids 字符串
        position_ids_str = request.POST.get('position_ids')
        if position_ids_str:
            # 将逗号分隔的字符串转换为整数列表
            position_ids = [int(pid) for pid in position_ids_str.split(',') if pid.isdigit()]

            positions = Position.objects.filter(id__in=position_ids)
            position_names = positions.values_list('position_name', flat=True)
            
            # 处理职位申请逻辑，例如：
            for pid in position_ids:
                # 例如：apply_to_position(pid)
                apply(request, pid)
            
            # 通过 Django 的 messages 传递信息
            messages.success(request, f"已成功申请以下岗位: {', '.join(position_names)}")
        else:
            messages.warning(request, "没有选择任何岗位")
        
        # 重定向到职位列表页面
        return redirect('/position/list/')  # 这里的 'position_list' 是路由名称，根据你的实际情况调整
    else:
        messages.error(request, "无效的请求方法")
        return redirect('list/')



# Create your views here.
def apply(request, pid):
    if request.method != "POST":
        return HttpResponse("不支持的请求类型")

    """申请职位视图"""
    # 获取职位和用户对象
    position_query_set = Position.objects.filter(id=pid)
    user_query_set = User.objects.filter(id=request.session.get("UserInfo").get("id"))
    resume_obj = Resume.objects.filter(id=request.POST.get("resume_id")).first()
    # 检查空值
    if not position_query_set:
        return render(request, 'UserAuth/alert_page.html', {"msg": "无效的岗位信息", "return_path": "/position/list/"})
    if not user_query_set:
        return render(request, 'UserAuth/alert_page.html', {"msg": "无效的用户身份", "return_path": "/position/list/"})
    # 选择对象
    position_obj = position_query_set.first()
    current_user_obj = user_query_set.first()
    # 检查用户选择的简历是不是自己的
    if resume_obj.belong_to.id != current_user_obj.id:
        return render(request, "UserAuth/alert_page.html", {'msg': "无权操作！"})
    # 检查岗位是否开放
    if not position_obj.published_state == 1:
        return render(request, 'UserAuth/alert_page.html', {"msg": "未开放的岗位", "return_path": "/position/list/"})
    # 检查是否未申请过
    application_query_set = Application.objects.filter(applicant=current_user_obj, position=position_obj)
    # 没有记录
    if not application_query_set:
        # 则写入新记录
        Application.objects.create(**{
            'applicant': current_user_obj,
            'position': position_obj,
            'application_time': timezone.localtime(),
            'create_time': timezone.localtime(),
            'resume': resume_obj,
        })
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "申请成功！", "return_path": "/position/view/{}/".format(pid), "success": True})

    # 如果有记录
    application_obj = application_query_set.first()
    if application_obj.active_state == 0:
        # 未生效则使之生效
        application_query_set.update(**{
            'application_time': timezone.localtime(),
            'active_state': 1,
            'resume': resume_obj,
        })
        return render(request, 'UserAuth/alert_page.html',
                  {"msg": "申请成功！", "return_path": "/position/view/{}/".format(pid)})

    # 已生效则无需更改
    return render(request, 'UserAuth/alert_page.html',
                  {"msg": "您已申请过该岗位！", "return_path": "/position/view/{}/".format(pid)})


def cancel(request, pid):
    """取消职位视图"""
    # 获取职位和用户对象
    position_query_set = Position.objects.filter(id=pid)
    user_query_set = User.objects.filter(id=request.session.get("UserInfo").get("id"))
    # 检查空值
    if not position_query_set:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "不合法的岗位！", "return_path": "/position/view/{}/".format(pid)})
    if not user_query_set:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "无效的用户信息！", "return_path": "/position/view/{}/".format(pid)})
    # 选择对象
    position_obj = position_query_set.first()
    user_obj = user_query_set.first()
    # 检查岗位是否开放
    if not position_obj.published_state == 1:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "未开放的岗位！", "return_path": "/position/view/{}/".format(pid)})
    # 检查是否已经申请过
    application_query_set = Application.objects.filter(applicant=user_obj, position=position_obj)
    if not application_query_set:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "不存在您的申请记录！", "return_path": "/position/view/{}/".format(pid)})
    # 通过检查
    data_dict = {
        'application_time': timezone.localtime(),
        'active_state': 0
    }
    application_query_set.update(**data_dict)
    return render(request, 'UserAuth/alert_page.html',
                  {"msg": "取消申请成功！", "return_path": "/position/view/{}/".format(pid)})


def hr_view_resume(request, uid, pid):
    """HR查看用户上传的简历"""
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    applicant_user_obj = User.objects.filter(id=uid).first()
    apply_position_obj = Position.objects.filter(id=pid).first()
    application_obj = Application.objects.filter(applicant=applicant_user_obj, position=apply_position_obj,
                                                 active_state=1).first()
    if not (current_user_obj and applicant_user_obj and apply_position_obj and application_obj):
        return render(request, 'UserAuth/alert_page.html', {"msg": "错误的参数。", "return_path": "/position/list/"})

    # 检查是否是HR身份
    if not current_user_obj.identity == 2:
        return render(request, "UserAuth/alert_page.html",
                      {'msg': '请使用HR身份登录', 'return_path': '/position/view/{}/'.format(pid)})

    # 检查是否是申请职位的HR
    if not current_user_obj.id == apply_position_obj.HR.id:
        return render(request, 'UserAuth/alert_page.html',
                      {'msg': "无权查看的内容！", 'return_path': '/position/view/{}/'.format(pid)})

    # 某用户申请某岗位的简历对象
    resume_obj = application_obj.resume
    file_path = os.path.join(settings.RESUME_ROOT, resume_obj.file_path)
    # 打开文件
    try:
        with open(file_path, 'rb') as f:
            # 读取文件内容
            file_data = f.read()
    except FileNotFoundError as e:
        return render(request, "UserAuth/alert_page.html",
                      {'msg': "文件已不存在，可能已被用户删除。", 'return_path': '/position/view/{}/'.format(pid)})
    response = HttpResponse(file_data, content_type='application/pdf')
    # 对文件名进行URL编码
    encoded_resume_id = urllib.parse.quote(resume_obj.name)
    # 设置响应的文件名，并指定字符编码
    response['Content-Disposition'] = 'inline; filename*=UTF-8\'\'{}'.format(encoded_resume_id)
    return response
