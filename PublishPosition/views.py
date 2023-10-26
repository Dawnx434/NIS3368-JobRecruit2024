from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
import markdown
from django.core.paginator import Paginator, EmptyPage

from PublishPosition.models import Position
from UserAuth.models import User
from Application.models import Application
from PublishPosition.utils.forms.MyForm import PublishPositionForm

from PublishPosition.utils.provincelist import province_dictionary
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

    # get query condition: Page and PageSize
    try:
        page = 1 if not request.GET.get('page') else int(request.GET.get('page'))
        pagesize = 10 if not request.GET.get('page_size') else int(request.GET.get('page_size'))
        keyword = '' if not request.GET.get('keyword') else request.GET.get('keyword')
        target_place = None if not request.GET.get('target_place') else int(request.GET.get('target_place'))
    except ValueError as e:
        return render(request, "UserAuth/alert_page.html", {"msg": '异常的查询参数', 'return_path': '/position/list/'})

    # get list
    if target_place:
        query_set = Position.objects.filter(published_state=1, position_name__contains=keyword, district=target_place)
    else:
        query_set = Position.objects.filter(published_state=1, position_name__contains=keyword)

    # filter according to query params
    paginator = Paginator(query_set, pagesize)
    # query_set = query_set[(page - 1) * pagesize: page * pagesize ]

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        current_page = paginator.page(page)
    except EmptyPage:
        current_page = paginator.page(1)

    page_title = f'"{keyword}" 的搜索结果' if keyword else '最新发布职位'
    context = {
        'query_set': current_page,
        'matching_files': matching_files[0],
        'district_dictionary': district_dictionary,
        'page_title': page_title,
        'keyword': keyword
    }
    return render(request, 'PublishPosition/position_list.html', context)


def view_position_detail(request, nid):
    """展示岗位的详细信息"""
    query_set = Position.objects.filter(id=nid)
    # 判空
    if not query_set:
        return render(request, 'UserAuth/alert_page.html',
                      {"msg": "不存在的或者未开放的岗位", "return_path": "/position/list/"})

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

    # 获取职位对象
    position = query_set.first()
    user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    # 未发布状态下，只有创建者且处于HR身份下可查看
    if position.published_state == 0:
        if not (user_obj.id == position.HR.id and user_obj.identity == 2):
            return render(request, 'UserAuth/alert_page.html',
                          {"msg": "不存在的或者未开放的岗位", "return_path": "/position/list/"})
    # 检查当前登录用户是否申请过该职位
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()
    position_query_set = Application.objects.filter(applicant=user_obj, position=position, active_state=1)

    context = {
        "matching_files": matching_files[0],
        "user_id": request.session.get("UserInfo")['id'],
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
        "already_apply": False if not position_query_set else True,
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
        return render(request, "UserAuth/alert_page.html",
                      {"msg": "您无权修改岗位信息", "return_path": "/position/list/"})

    if request.method == 'GET':
        # 获取属性内容['position_name', 'salary', 'summary', 'detail', 'province', 'published_state']
        data_dict = {
            'position_name': position_obj.position_name,
            'salary': position_obj.salary,
            'summary': position_obj.summary,
            'detail': position_obj.detail,
            'district': position_obj.district,
            'published_state': position_obj.published_state
        }
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict,
            "matching_files": matching_files[0],
        }

        return render(request, "PublishPosition/position_modify.html", context)

    # else POST
    data_dict = {}
    error_dict = {}
    # 提取数据
    for field in ['position_name', 'salary', 'summary', 'detail', 'district', 'published_state']:
        data_dict[field] = request.POST.get(field)
    # 检查字段
    data_dict, error_dict, check_passed_flag = check_publish_position_form(data_dict)
    if not check_passed_flag:
        # 未通过检查
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict,
            'error_dict': error_dict,
            "matching_files": matching_files[0],
        }
        return render(request, "PublishPosition/position_modify.html", context)

    # 通过字段检查
    query_set.update(**data_dict)
    # 确认返回页面
    if data_dict['published_state'] == 1:
        # 如果仍然可见
        return redirect('/position/view/{}/'.format(nid))
    else:
        return render(request, "UserAuth/alert_page.html",
                      {"msg": "岗位信息已不可见，请前往用户中心-我发布的职位中查看", "return_path": "/position/list/"})
