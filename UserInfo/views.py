import datetime
import os
import re

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

from UserAuth.utils.generateCode import send_sms_code
from UserAuth.utils import validators
from UserAuth.models import User
from Application.models import Application
from PublishPosition.models import Position
from UserInfo.models import Resume


# Create your views here.
def index(request, pk):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    matching_files = find_image(request)

    # 查询并返回数据
    query_set = User.objects.filter(id=pk)
    # 获取用户数据
    obj = query_set.first()

    topic_per_page = 5
    topic = obj.topics.order_by('last_updated')
    topic_paginator = Paginator(topic, topic_per_page)
    topic_page_number = request.GET.get('topic_page')
    show_topic_page = topic_page_number is not None
    try:
        topic_current_page = topic_paginator.get_page(topic_page_number)
    except EmptyPage:
        topic_current_page = topic_paginator.page(topic_paginator.num_pages)

    is_hr = obj.hr_allowed == 3  # 具有HR资格就要显示其发布的岗位

    user_info = {
        "id": pk,
        "username": obj.username,
        "mobile_phone": obj.mobile_phone,
        "gender": obj.get_gender_display(),
        "email": obj.email,
        "edu_ground": obj.edu_ground,
        "school": obj.school,
        "major": obj.major,
        "excepting_position": obj.excepting_position,
        "excepting_location": obj.excepting_location,
        "matching_files": matching_files,
        'topics': topic_current_page,
        'show_position': show_topic_page,
        'initial_position': request.GET.get('scrollPosition'),
        'scroll_to_bottom': show_topic_page,
        'is_hr': is_hr,
    }

    if is_hr:
        position_per_page = 6
        position = obj.positions.filter(published_state=1)
        position_paginator = Paginator(position, position_per_page)
        position_page_number = request.GET.get('position_page')
        show_position_page = position_page_number is not None
        try:
            position_current_page = position_paginator.get_page(position_page_number)
        except EmptyPage:
            position_current_page = position_paginator.page(position_paginator.num_pages)

        scroll_to_bottom = show_topic_page or show_position_page

        user_info['scroll_to_bottom'] = scroll_to_bottom
        user_info['positions'] = position_current_page
        user_info['show_position'] = show_position_page

    return render(request, "UserInfo/index.html", context=user_info)


def resume(request):
    # 查询当前用户的所有简历
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    resume_query_set = Resume.objects.filter(belong_to=current_user_obj)
    resume_list = []
    for resume_obj in resume_query_set:
        resume_list.append({
            "id": resume_obj.id,
            "name": resume_obj.name
        })
    context = {"resumes": resume_list}
    return render(request, "UserInfo/resume.html", context=context)


def apply(request):
    """查看申请历史记录"""
    # 获取用户信息
    user_obj = User.objects.filter(id=request.session.get('UserInfo').get("id")).first()
    # 筛选用户申请记录
    position_query_set = Application.objects.filter(applicant=user_obj, active_state=1)
    # 转化为列表供前端渲染
    position_list = []
    for obj in position_query_set:
        list_obj = {
            'position_id': obj.position.id,
            'position_name': obj.position.position_name,
            'application_time': (obj.application_time + datetime.timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M"),
        }
        position_list.append(list_obj)

    context = {
        'position_list': position_list,
    }

    return render(request, 'UserInfo/user_application.html', context)


def account(request):
    """修改用户敏感数据"""
    # 获取用户对象
    user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()

    if request.method == 'GET':
        data_dict = {
            'username': user_obj.username,
            'mobile_phone': user_obj.mobile_phone,
            'email': user_obj.email,
            'identity': user_obj.get_identity_display()
        }
        context = {
            'data_dict': data_dict
        }
        return render(request, "UserInfo/user_account.html", context=context)

    # else POST
    error_dict = {}
    fields = ['username', 'password', 'confirm_password', 'mobile_phone', 'email', 'verification_code']
    post_data = {}
    for field in fields:
        post_data[field] = request.POST.get(field)
    # 校验字段值
    check_passed = True
    # check username 唯一性/不包含特殊字符
    user_query_set = User.objects.filter(username=post_data['username'])
    if user_query_set and user_query_set.first().id != user_obj.id:
        # 存在其他用户具有相同的用户名
        error_dict['username'] = "用户名已存在"
        check_passed = False
    if not validators.is_username_valid(post_data['username']):
        error_dict['username'] = "用户名只能包含数字和字母"
        check_passed = False

    # check password and confirm_password
    if post_data['password'] or post_data['confirm_password']:
        if post_data['password'] != post_data['confirm_password']:
            error_dict['confirm_password'] = "两次密码不一致"
            check_passed = False

    # check mobile_phone and email
    if not validators.is_valid_email(post_data['email']):
        error_dict['email'] = "非法的邮箱格式"
        check_passed = False
    if not validators.is_mobile_phone_valid(post_data['mobile_phone']):
        error_dict['mobile_phone'] = "非法的手机号格式"
        check_passed = False

    # check verification_code
    if post_data['verification_code'] != request.session.get("account_verification_code"):
        error_dict['verification_code'] = "验证码错误"
        check_passed = False

    if not check_passed:
        return render(request, "UserInfo/user_account.html", {"data_dict": post_data, "error_dict": error_dict})

    # ready to save
    save_data = {
        'username': post_data['username'],
        'mobile_phone': post_data['mobile_phone'],
        'email': post_data['email']
    }
    if post_data['password']:
        save_data['password'] = post_data['password']
    print(save_data)
    User.objects.filter(id=request.session.get("UserInfo").get("id")).update(**save_data)
    return redirect("/info/info/")


@csrf_exempt
def sendemail(request):
    if not request.method == "POST":
        return JsonResponse({
            'state': False,
            'msg': "Invalid request method!"
        })

    # else POST
    user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    new_email = request.POST.get("new_email_address")
    data_dict = {}
    # 发送邮箱验证码
    state, code = send_sms_code(user_obj.email)
    if not state:
        data_dict['state'] = False
        data_dict['msg'] = '邮件发送失败，请稍后重试'

    # state = True
    request.session['account_verification_code'] = code
    request.session.set_expiry(5 * 60)  # 5分钟有效期
    data_dict['state'] = True
    if user_obj.email == new_email:
        data_dict['msg'] = "邮件已发送至{}".format(user_obj.email)
    else:
        data_dict['msg'] = "此次修改设置了新邮箱{}，请注意检查！".format(new_email)

    return JsonResponse(data_dict)


def image_upload(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('upload')
        if not upload_image:
            return render(request, 'UserInfo/upload_avatar_result.html', {'message': '没有上传头像', 'success': False})
        # 获取上传文件的后缀名
        file_extension = os.path.splitext(upload_image.name)[1]
        # 这里对文件后缀名进行检验、设置白名单
        white_list = {'.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tiff', '.svg'}
        if file_extension not in white_list:
            return render(request, 'UserInfo/upload_avatar_result.html',
                          {'message': '你上传的文件格式不正确', 'success': False})
        # 将原有图像进行删除
        pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
        file_names = os.listdir(settings.PROFILE_ROOT)
        matching_files = []
        for file_name in file_names:
            if pattern.match(file_name):
                matching_files.append(file_name)
                os.remove(settings.PROFILE_ROOT + file_name)
        save_path = os.path.join(settings.PROFILE_ROOT, str(request.session['UserInfo'].get("id")) + file_extension)
        # 保存文件到指定位置
        with open(save_path, 'wb') as file:
            for chunk in upload_image.chunks():
                file.write(chunk)
        return render(request, 'UserInfo/upload_avatar_result.html', {'message': '头像上传成功', 'success': True})
    else:
        return render(request, 'UserInfo/upload_avatar_result.html', {'message': '头像上传失败', 'success': False})


def modify(request):
    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return HttpResponse("不合法的身份")
    # 获取用户数据
    obj = query_set.first()
    user_info = {"id": request.session['UserInfo'].get("id"),
                 "username": obj.username,
                 "mobile_phone": obj.mobile_phone,
                 "gender": obj.get_gender_display(),
                 "email": obj.email,
                 "edu_ground": obj.edu_ground,
                 "school": obj.school,
                 "major": obj.major,
                 "excepting_position": obj.excepting_position,
                 "excepting_location": obj.excepting_location
                 }
    context = {
        'userinfo': user_info
    }
    return render(request, "UserInfo/userinfo_modify.html", context)


def my_published_position(request):
    """返回我发布的职位"""
    user_query_set = User.objects.filter(id=request.session.get("UserInfo").get("id"))
    if not user_query_set:
        return render(request, "UserAuth/alert_page.html", {"msg": "不合法的身份"})
    user_obj = user_query_set.first()
    if user_obj.identity != 2:
        return render(request, "UserAuth/alert_page.html", {"msg": "请先至账号安全处切换至HR身份！"})
    position_query_set = Position.objects.filter(HR=user_obj)
    position_list = []
    for position in position_query_set:
        position_list.append({
            "position_id": position.id,
            "position_name": position.position_name,
            "published_state": position.get_published_state_display()
        })

    context = {
        "position_list": position_list
    }

    return render(request, "UserInfo/my_published_position.html", context)


def info(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    matching_files = find_image(request)
    if request.method == "GET":
        # 查询并返回数据
        query_set = User.objects.filter(id=request.session["UserInfo"].get("id"))
        # 获取用户数据
        obj = query_set.first()
        user_info = {"id": request.session['UserInfo'].get("id"),
                     "username": obj.username,
                     "mobile_phone": obj.mobile_phone,
                     "gender": obj.get_gender_display(),
                     "email": obj.email,
                     "edu_ground": obj.edu_ground,
                     "school": obj.school,
                     "major": obj.major,
                     "excepting_position": obj.excepting_position,
                     "excepting_location": obj.excepting_location,
                     "matching_files": matching_files,
                     }
        return render(request, "UserInfo/userinfo.html", context=user_info)
    # else POST
    data = request.POST
    fields = ['username', 'mobile_phone', 'gender', 'email',
              'edu_ground', 'school', 'major', 'excepting_position', 'excepting_location']
    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return HttpResponse("不合法的身份")
    # 获取用户数据
    obj = query_set.first()

    for field in fields:
        # print('field: ', data.get(field))
        setattr(obj, field, data.get(field))
    obj.save()
    # print('obj.school: ', obj.school)
    user_info = {"id": request.session['UserInfo'].get("id"),
                 "username": obj.username,
                 "mobile_phone": obj.mobile_phone,
                 "gender": obj.get_gender_display(),
                 "email": obj.email,
                 "edu_ground": obj.edu_ground,
                 "school": obj.school,
                 "major": obj.major,
                 "excepting_position": obj.excepting_position,
                 "excepting_location": obj.excepting_location,
                 "matching_files": matching_files,
                 }
    return render(request, "UserInfo/userinfo.html", context=user_info)


def resume_upload(request):
    current_user_obj = User.objects.filter(id=request.session['UserInfo'].get("id")).first()
    if request.method == 'POST':
        resume_name = request.POST.get("resume_name")
        upload_resume = request.FILES.get('upload')
        if not upload_resume:
            context = {'msg': '您没有上传您的简历文件', 'success': False}
            return render(request, "UserInfo/upload_resume_result.html", context=context)
        save_directory = os.path.join(settings.RESUME_ROOT + str(current_user_obj.id))
        # 不存在文件夹，则创建
        if not os.path.exists(save_directory):
            os.mkdir(save_directory)

        save_path = os.path.join(save_directory, upload_resume.name)
        # 这里对文件后缀名进行检验、设置白名单
        file_extension = os.path.splitext(upload_resume.name)[1]
        white_list = {'.pdf'}
        if file_extension not in white_list:
            context = {'msg': '你上传的文件格式不对,请上传pdf格式的简历', 'success': False}
            return render(request, "UserInfo/upload_resume_result.html", context=context)

        # 保存文件和数据库对应关系
        save_file_path = "{}/{}".format(str(current_user_obj.id), upload_resume.name)
        Resume.objects.create(name=resume_name, file_path=save_file_path, belong_to=current_user_obj)

        with open(save_path, 'wb') as file:
            for chunk in upload_resume.chunks():
                file.write(chunk)
        context = {'msg': '上传简历成功', 'success': True}
        return render(request, "UserInfo/upload_resume_result.html", context=context)


def resume_download(request):
    resume_id = request.GET.get('resume_id')
    # 获取用户对象
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    # 找到resume对象
    try:
        resume_obj = Resume.objects.filter(id=resume_id).first()
    except BaseException as e:
        return HttpResponse("找不到对象！")

    # 检查用户是否是简历的上传者
    if current_user_obj.id != resume_obj.belong_to.id:
        return render(request, "UserAuth/alert_page.html", {"msg": "无权查看的页面！"})

    file_path = os.path.join(settings.RESUME_ROOT, resume_obj.file_path)
    # 打开文件
    with open(file_path, 'rb') as f:
        # 读取文件内容
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/pdf')
    # 对文件名进行URL编码
    encoded_resume_id = urllib.parse.quote(resume_id)
    # 设置响应的文件名，并指定字符编码
    response['Content-Disposition'] = 'inline; filename*=UTF-8\'\'{}'.format(encoded_resume_id)
    return response


def remove_resume(request, rid):
    """删除简历"""
    # 获取对象
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    resume_obj = Resume.objects.filter(id=rid).first()
    # 判空
    if not (current_user_obj and resume_obj):
        return render(request, "UserAuth/alert_page.html", {"msg": "无效的参数", "return_path": "/info/resume/"})

    # 判断resume归属
    if current_user_obj.id != resume_obj.belong_to.id:
        return render(request, "UserAuth/alert_page.html", {"msg": "你无权操作！", "return_path": "/info/resume/"})

    # 执行删除
    file_name = resume_obj.name
    file_path = os.path.join(settings.RESUME_ROOT, resume_obj.file_path)
    os.remove(file_path)
    Resume.objects.filter(id=rid).delete()

    return render(request, "UserAuth/alert_page.html", {'msg': "已删除简历{}".format(file_name),'return_path': '/info/resume/'})


def show_index(request):
    # 用GET获取用户name
    guest_name = request.GET.get('guest_name')
    query_set = User.objects.filter(username=guest_name)
    obj = query_set.first()
    img = find_image(request)
    # 获取头像
    if not obj:
        return render(request, "UserAuth/alert_page.html", {'msg': '不合法的用户名称'})

    name = request.session.get("UserInfo")
    context = {"username": guest_name,
               'image': img}
    return render(request, "UserInfo/show_index.html", context)


def find_image(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
    return matching_files[0]
