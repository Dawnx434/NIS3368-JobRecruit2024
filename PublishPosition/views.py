from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import markdown
from django.core.paginator import Paginator, EmptyPage

from PublishPosition.models import Position
from UserAuth.models import User
from Application.models import Application
from UserInfo.models import Resume
from PublishPosition.forms import PublishPositionForm

from PublishPosition.utils.district import district_dictionary
from PublishPosition.utils.check_position_form import check_publish_position_form

import os
from django.conf import settings
import re


# Create your views here.
def position_list(request):
    """返回职位列表"""
    # 获取头像
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')

    # 获取查询参数
    try:
        page = int(request.GET.get('page', 1))
        pagesize = int(request.GET.get('page_size', 10))
        keyword = request.GET.get('keyword', '')
        target_place = request.GET.get('target_place', None)  # 这里保持为 None，后续处理
    except ValueError:
        return render(request, "UserAuth/alert_page.html", {"msg": '异常的查询参数', 'return_path': '/position/list/'})

    # 获取职位列表
    query_set = search_positions(keyword, target_place)

    # 排序
    query_set = query_set.order_by('salary')
    paginator = Paginator(query_set, pagesize)

    try:
        current_page = paginator.page(page)
    except EmptyPage:
        current_page = paginator.page(1)
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    resume_query_set = Resume.objects.filter(belong_to=current_user_obj)
    resumes = []
    for resume_obj in resume_query_set:
        resumes.append({
            "id": resume_obj.id,
            "name": resume_obj.name
        })

    position_ids = list(query_set.values_list('id', flat=True))
    position_names = list(query_set.values_list('position_name', flat=True))
    page_title = f'职位 "{keyword}" 的搜索结果' if keyword else '最新发布职位'
    context = {
        'query_set': current_page,
        'position_names':position_names,
        'position_ids': position_ids,
        'matching_files': matching_files[0],
        'district_dictionary': district_dictionary,
        'page_title': page_title,
        'keyword': keyword,
        'resumes':resumes
        'target_place': target_place #ToDo:wating for check
    }
    return render(request, 'PublishPosition/position_list.html', context)


def search_positions(keyword, target_place):
    """根据条件搜索岗位"""
    filters = {'published_state': 1}
    if keyword:
        filters['position_name__contains'] = keyword
    if target_place:
        filters['district'] = target_place

    return Position.objects.filter(**filters)



def view_position_detail(request, nid):
    """展示岗位的详细信息"""
    query_set = Position.objects.filter(id=nid)
    # 判空
    if not query_set:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "不存在的岗位", "return_path": "/position/list/"})
    # 获取对象
    position = query_set.first()
    current_user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    application_query_set = Application.objects.filter(applicant=current_user_obj, position=position, active_state=1)
    # 申请了该岗位的用户列表
    user_has_applied_list = []
    for user in User.objects.all():
        if Application.objects.filter(applicant=user, position=position, active_state=1):
            user_has_applied_list.append({
                "user_id": user.id,
                "username": user.username
            })
    # 获取用户头像
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
    # 获取HR头像
    HR_pattern = re.compile(str(position.HR.id) + r'.*')
    HR_matching_files = []
    for file_name in file_names:
        if HR_pattern.match(file_name):
            HR_matching_files.append(file_name)
    # 没有上传就用默认的
    if not HR_matching_files:
        HR_matching_files.append('default.jpeg')

    # 未发布状态下，只有创建者且处于HR身份下可查看
    if position.published_state == 0:
        if not ((current_user_obj.id == position.HR.id and current_user_obj.identity == 2) or application_query_set.exists()):
            return render(request, 'UserAuth/alert_page.html',
                          {"msg": "未开放的岗位", "return_path": "/position/list/"})

    # 用户可用的简历
    resume_query_set = Resume.objects.filter(belong_to=current_user_obj)
    resumes = []
    for resume_obj in resume_query_set:
        resumes.append({
            "id": resume_obj.id,
            "name": resume_obj.name
        })
    context = {
        "matching_files": matching_files[0],
        "HR_matching_files": HR_matching_files[0],
        "user_id": request.session.get("UserInfo")['id'],
        "HR_user_id": position.HR.id,
        "position_id": position.id,
        "position_name": position.position_name,
        "salary": position.salary,
        "summary": position.summary,
        "detail": mark_safe(markdown.markdown(position.detail,
                                              extensions=[
                                                  'markdown.extensions.extra',
                                                  'markdown.extensions.codehilite',
                                                  'markdown.extensions.toc',
                                              ])),
        # "detail": position.detail,
        "HR": position.HR,
        "district": position.get_district_display(),
        "already_apply": False if not application_query_set else True,
        "publish_state": position.published_state,
        "user_has_applied_list": user_has_applied_list,
        "resumes": resumes
    }

    return render(request, "PublishPosition/position_detail.html", context)


def publish_position(request):
    # Publish Position理应只能HR身份登录，因此优先校验是否是HR身份
    # 获取当前登录用户信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()
    # 检查发布职位者的身份是否为HR
    if user_obj.identity != 2:
        # 当前登录用户非HR身份
        return render(request, "UserAuth/alert_page.html", {"msg": "请使用HR身份登录", "return_path": "/info/account/"})

    # 获取头像
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')

    if request.method == 'GET':
        form = PublishPositionForm()
        context = {
            'district_dictionary': district_dictionary,
            "matching_files": matching_files[0],
        }
        return render(request, "PublishPosition/position_publish.html", context)

    # else POST
    data_dict = {}
    error_dict = {}
    for field in ['position_name', 'salary', 'summary', 'detail', 'district', 'published_state']:
        data_dict[field] = request.POST.get(field)

    # print(data_dict['detail'])
    # 补充字段
    data_dict['HR'] = user_obj

    # 字段校验
    data_dict, error_dict, check_passed_flag = check_publish_position_form(data_dict)

    print(check_passed_flag)
    if not check_passed_flag:
        # 未通过检查
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict,
            'error_dict': error_dict,
            "matching_files": matching_files[0],
        }
        return render(request, "PublishPosition/position_publish.html", context)

    # 通过字段检查
    Position.objects.create(**data_dict)
    return redirect('/position/list/')


def modify_position(request, nid):
    query_set = Position.objects.filter(id=nid)
    if not query_set:
        return render(request, "UserAuth/alert_page.html",
                      {"msg": "不存在的岗位信息", "return_path": "/position/list/"})
    # 获取目标岗位对象
    position_obj = query_set.first()
    # 获取当前登录用户信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()

    # 获取头像
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')

    # 检查发布职位者的身份是否为HR
    if user_obj.identity != 2:
        # 当前登录用户非HR身份
        return render(request, "UserAuth/alert_page.html", {"msg": "请使用HR身份登录", "return_path": "/info/account/"})
    # 检查当前用户是否具有编辑权限
    if request.session.get("UserInfo")['id'] != position_obj.HR_id:
        return render(request, "UserAuth/alert_page.html", {"msg": "您没有权限编辑该岗位", "return_path": "/position/list/"})

    # 表单提交
    if request.method == 'POST':
        # 保存修改
        position_obj.position_name = request.POST.get('position_name')
        position_obj.salary = request.POST.get('salary')
        position_obj.summary = request.POST.get('summary')
        position_obj.detail = request.POST.get('detail')
        position_obj.district = request.POST.get('district')
        position_obj.published_state = request.POST.get('published_state')
        position_obj.save()
        return redirect('/position/list/')

    # 表单渲染
    context = {
        'district_dictionary': district_dictionary,
        'matching_files': matching_files[0],
        'position_obj': position_obj
    }
    return render(request, "PublishPosition/position_modify.html", context)


def delete_position(request, nid):
    """删除岗位"""
    query_set = Position.objects.filter(id=nid)
    if not query_set:
        return render(request, "UserAuth/alert_page.html",
                      {"msg": "不存在的岗位信息", "return_path": "/position/list/"})
    # 获取目标岗位对象
    position_obj = query_set.first()
    # 获取当前登录用户信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()

    # 检查发布职位者的身份是否为HR
    if user_obj.identity != 2:
        # 当前登录用户非HR身份
        return render(request, "UserAuth/alert_page.html", {"msg": "请使用HR身份登录", "return_path": "/info/account/"})
    # 检查当前用户是否具有删除权限
    if request.session.get("UserInfo")['id'] != position_obj.HR_id:
        return render(request, "UserAuth/alert_page.html", {"msg": "您没有权限删除该岗位", "return_path": "/position/list/"})

    position_obj.delete()
    return redirect('/position/list/')
