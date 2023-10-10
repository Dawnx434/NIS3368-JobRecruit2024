from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from UserAuth.utils.Forms import RegisterForm, LoginForm

from UserAuth import models

from UserAuth.utils.generateCode import check_code, send_sms_code
from UserAuth.utils.validators import is_valid_email


# Create your views here.
def register(request):
    if request.method == 'GET':
        form = RegisterForm(request=request)
        context = {
            'form': form,
            'nid': 1  # represent registration
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # if method is post
    form = RegisterForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 1
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # store userinfo
    form.instance.identity = 1  # default: User
    form.save()

    # generate cookie
    obj = models.User.objects.filter(username=form.cleaned_data["username"]).first()
    request.session["UserInfo"] = {
        'id': obj.id,
        'username': obj.username
    }
    request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
    return redirect("/")


def login(request):
    if request.method == 'GET':
        form = LoginForm(request=request)
        context = {
            'form': form,
            'nid': 2
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # if method is POST
    form = LoginForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 2
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    row_obj = models.User.objects.filter(username=form.cleaned_data['username']).first()
    request.session["UserInfo"] = {
        'id': row_obj.id,
        'username': row_obj.username
    }
    request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
    return redirect('/info/info')


def logout(request):
    request.session.clear()
    return redirect("/")


def checkLoginState(request):
    user_info = request.session.get("UserInfo")
    if not user_info:
        return HttpResponse("您尚未登录")

    return HttpResponse("Welcome User: " + user_info["username"])


def generate_verification_code(request):
    stream = BytesIO()
    img, code = check_code()
    # img 储存到内存流中
    img.save(stream, 'png')
    request.session["verification_code"] = code
    request.session.set_expiry(120)  # 验证码60秒有效期
    return HttpResponse(stream.getvalue())


@csrf_exempt
def sendemail(request):
    if request.method == 'GET':
        data = {
            'state': False,
            'msg': 'Invalid request method'
        }
        return JsonResponse(data)

    email = request.POST.get('email_address')
    if not is_valid_email(email):
        data = {
            'state': False,
            'msg': 'Invalid Email format'
        }
        return JsonResponse(data)
    else:
        # 发送邮件
        state, code = send_sms_code(target_email=email)
        request.session['verification_code'] = code
        request.session.set_expiry(2 * 60)
        data = {
            'state': True,
            'msg': 'Send Email successfully'
        }
        return JsonResponse(data)


def index(request):
    userinfo = request.session.get("UserInfo")
    context = {
        'username': userinfo
    }
    return render(request, 'UserAuth/index.html', context=context)
