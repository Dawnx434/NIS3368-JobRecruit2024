from django.shortcuts import render, redirect, HttpResponse
from UserAuth.models import User


# Create your views here.
def index(request):
    name = request.session.get("UserInfo")
    context = {"username": name}
    return render(request, "index.html", context)


def resume(request):
    return 1


def apply(request):
    return 1


def account(request):
    return 1


def modify(request):
    if request.method == "GET":
        # 查询并返回数据
        query_set = User.objects.filter(id=request.session["UserInfo"].get("id"))
        # 判空
        if not query_set:
            return HttpResponse("不合法的身份")
        obj = query_set.first()
        user_info = {("username", "用户名"): obj.username,
                     ("mobile_phone", "手机号"): obj.mobile_phone,
                     ("gender", "性别"): obj.gender,
                     ("email", "邮箱"): obj.email,
                     ("edu_ground", "学历"): obj.edu_ground,
                     ("school", "毕业院校"): obj.school,
                     ("major", "专业"): obj.major,
                     ("excepting_position", "期望职位"): obj.excepting_position,
                     ("excepting_location", "期望地址"): obj.excepting_location
                     }
        context = {
            'userinfo': user_info
        }
        return render(request, "userinfo_modify.html", context)

    # else POST
    data = request.POST
    fields = ['username', 'mobile_phone', 'gender', 'email',
              'edu_ground', 'school', 'major', 'excepting_position', 'excepting_location']
    new_info = {}
    for field in fields:
        new_info[field] = data.get(field)

    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return HttpResponse("不合法的身份")
    query_set.update(**new_info)

    return redirect("/info/index/")


def change_sql():
    return 1
