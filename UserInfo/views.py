import datetime
from django.shortcuts import render, redirect, HttpResponse
from UserAuth.models import User
from PublishPosition.models import Position
from Application.models import Application
from django.http import JsonResponse, FileResponse, Http404
import os
import glob
from django.conf import settings
import re
import random
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from UserAuth.utils.generateCode import send_sms_code
from UserAuth.utils import validators


# Create your views here.
def index(request, pk):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    matching_files = find_image(request)
    if request.method == "GET":
        # 查询并返回数据
        query_set = User.objects.filter(id=pk)
        # 获取用户数据
        obj = query_set.first()
        user_info = {"id": pk,
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
                     'topics': obj.topics.all(),
                     'positions': obj.positions.all(),
                     }
        return render(request, "UserInfo/index.html", context=user_info)
    # else POST
    data = request.POST
    fields = ['username', 'mobile_phone', 'gender', 'email',
              'edu_ground', 'school', 'major', 'excepting_position', 'excepting_location']
    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return render(request, "UserAuth/alert_page.html", {'msg': "不合法的身份"})
    # 获取用户数据
    obj = query_set.first()
    for field in fields:
        setattr(obj, field, data.get(field))
    obj.save()
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
    return render(request, "UserInfo/index.html", context=user_info)


def resume(request):
    id = str(request.session['UserInfo'].get("id"))
    save_path = os.path.join(settings.RESUME_ROOT + id)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    file_names = os.listdir(save_path)
    file_position = [os.path.join(save_path, filename) for filename in file_names]
    image = find_image(request)
    lenth = len(file_names)
    context = {"resumes": file_names,
               "id": id,
               'file_position': file_position,
               'length': lenth,
               'image': image}
    return render(request, "UserInfo/resume.html", context=context)


def apply(request):
    """查看申请历史记录"""
    # 获取用户信息
    user_obj = User.objects.filter(id=request.session.get('UserInfo').get("id")).first()
    # 筛选用户申请记录
    position_query_set = Application.objects.filter(applicant=user_obj)
    # 转化为列表供前端渲染
    position_list = []
    for obj in position_query_set:
        list_obj = {
            'id': obj.id,
            'applicant': obj.applicant.username,
            'position_id': obj.position.id,
            'position_name': obj.position.position_name,
            'application_time': (obj.application_time + datetime.timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M:%S"),
            'application_state': obj.get_active_state_display(),
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
            "id": position.id,
            "position_name": position.position_name,
            "summary": position.summary if len(position.summary) < 40 else position.summary[0:40] + "...",
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
        setattr(obj, field, data.get(field))
    obj.save()
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
    if request.method == 'POST':
        upload_resume = request.FILES.get('upload')
        if not upload_resume:
            context = {'msg': '您没有上传您的简历文件', 'success': False}
            return render(request, "UserInfo/upload_resume_result.html", context=context)
        save_path = os.path.join(settings.RESUME_ROOT + str(request.session['UserInfo'].get("id")))
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        matching_files = os.listdir(save_path)
        lengh = len(matching_files)
        save_path = os.path.join(save_path, upload_resume.name)
        file_extension = os.path.splitext(upload_resume.name)[1]
        # 这里对文件后缀名进行检验、设置白名单
        white_list = {'.pdf'}
        if file_extension not in white_list:
            context = {'msg': '你上传的文件格式不对,请上传pdf格式的简历', 'success': False}
            return render(request, "UserInfo/upload_resume_result.html", context=context)
        save_path = os.path.join(save_path)
        # 保存文件
        with open(save_path, 'wb') as file:
            for chunk in upload_resume.chunks():
                file.write(chunk)
        context = {'msg': '上传简历成功', 'success': True}
        return render(request, "UserInfo/upload_resume_result.html", context=context)


def resume_download(request):
    resume_id = request.GET.get('resume_id')
    download_path = os.path.join(settings.RESUME_ROOT, str(request.session['UserInfo'].get("id")))
    download_path = os.path.join(download_path, resume_id)
    # 打开文件
    with open(download_path, 'rb') as f:
        # 读取文件内容
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/pdf')
    # 对文件名进行URL编码
    encoded_resume_id = urllib.parse.quote(resume_id)
    # 设置响应的文件名，并指定字符编码
    response['Content-Disposition'] = 'inline; filename*=UTF-8\'\'{}'.format(encoded_resume_id)
    return response


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
