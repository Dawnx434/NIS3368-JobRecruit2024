from django.shortcuts import render, redirect, HttpResponse
from UserAuth.models import User
from django.http import JsonResponse, FileResponse, Http404
import os
import glob
from django.conf import settings
import re
import random
import urllib.parse


# Create your views here.
def index(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
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
                     "matching_files": matching_files[0],
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
                 "matching_files": matching_files[0],
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
    context = {"resumes": file_names ,
               "id": id,
               'file_position':file_position,
               'length':lenth,
               'image':image}
    return render(request, "UserInfo/resume.html", context=context)


def apply(request):
    return 1


def account(request):
    return 1


def image_upload(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('upload')
        if not upload_image:
            return render(request, 'UserInfo/upload_avatar_result.html',{'message':'没有上传头像', 'success': False})
        # 获取上传文件的后缀名
        file_extension = os.path.splitext(upload_image.name)[1]
        # 这里对文件后缀名进行检验、设置白名单
        white_list = {'.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tiff', '.svg'}
        if file_extension not in white_list:
            return render(request, 'UserInfo/upload_avatar_result.html',{'message':'你上传的文件格式不正确', 'success': False})
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
        return render(request, 'UserInfo/upload_avatar_result.html',{'message':'头像上传成功', 'success': True})
    else:
        return render(request, 'UserInfo/upload_avatar_result.html',{'message':'头像上传失败', 'success': False})


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


def info(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
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
                     "matching_files": matching_files[0],
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
                 "matching_files": matching_files[0],
                 }
    return render(request, "UserInfo/userinfo.html", context=user_info)


def resume_upload(request):
    if request.method == 'POST':
        upload_resume = request.FILES.get('upload')
        if not upload_resume:
            context = {'msg':'没有上传简历','success':False}
            return render(request,"UserInfo/upload_resume_result.html",context=context)
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
        save_path = os.path.join(save_path )
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
        return HttpResponse('用户昵称错误')

    name = request.session.get("UserInfo")
    context = {"username": guest_name,
               'image':img}
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