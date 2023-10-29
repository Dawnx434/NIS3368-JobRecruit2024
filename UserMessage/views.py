import datetime

from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage

from UserAuth.models import User
from UserMessage.models import Message

from markdown import markdown


# Create your views here.
def send_message(request):
    """发送私信"""
    if request.method == "GET":
        try:
            reply_to = int(request.GET.get("reply"))
            message_query_set = Message.objects.filter(id=reply_to)
        except BaseException as e:
            reply_to = None

        if not reply_to:
            return render(request, "UserMessage/send_message.html")

        # 有则证明是回复私信
        message_obj = message_query_set.first()
        origin_title = message_obj.title
        title = '回复：' + origin_title
        data_dict = {
            "to_user": message_obj.from_user.username,
            "title": title,
            "reply_to": reply_to
        }
        context = {
            "data_dict": data_dict
        }
        return render(request, "UserMessage/send_message.html", context)

    # else POST
    fields = ['to_user', 'title', 'content', 'reply_to']
    data_dict = {}
    error_dict = {}
    for field in fields:
        data_dict[field] = request.POST.get(field)

    # begin check
    check_passed_flag = True
    # 查询用户名是否存在
    to_user_query_set = User.objects.filter(username=data_dict["to_user"])
    if not to_user_query_set:
        error_dict['to_user'] = "不存在此用户"
        check_passed_flag = False
    # 检查标题长度是否符合要求
    print(data_dict['title'])
    print(len(data_dict['title']))
    if not 0 < len(data_dict['title']) <= 100:
        error_dict['title'] = '标题长度需在1至100字符之间'
        check_passed_flag = False
    if not 0 < len(data_dict['content']) <= 2000:
        error_dict['content'] = "内容长度需在1至2000字符"
        check_passed_flag = False

    context = {
        "data_dict": data_dict,
        "error_dict": error_dict,
    }
    if not check_passed_flag:
        return render(request, "UserMessage/send_message.html", context)

    # 检查回复私信字段是否合理
    try:
        reply_to = int(data_dict['reply_to'])
        reply_to = Message.objects.filter(id=reply_to).first()
    except BaseException as e:
        reply_to = None

    Message.objects.create(
        to_user=to_user_query_set.first(),
        from_user=User.objects.filter(id=request.session.get("UserInfo").get("id")).first(),
        title=data_dict['title'],
        content=data_dict['content'],
        create_time=timezone.localtime(),
        reply_to=reply_to,
    )

    context_result = {
        'msg': '私信发送成功！',
        'return_path': '/message/list/',
        'success': True,
    }
    return render(request, "UserAuth/alert_page.html", context_result)


def message_list(request):
    """展示用户当前收到的所有私信"""
    user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    # 收到的私信和发出的私信
    message_query_set_as_recipient = Message.objects.filter(to_user=user_obj)
    message_query_set_as_sender = Message.objects.filter(from_user=user_obj)
    # 分页
    mails_per_page = 9
    recipient_paginator = Paginator(message_query_set_as_recipient, mails_per_page)
    sender_paginator = Paginator(message_query_set_as_sender, mails_per_page)
    recipient_page_number = request.GET.get('receive_page')
    sender_page_number = request.GET.get('send_page')
    show_recipient_page = recipient_page_number is not None
    show_sender_page = sender_page_number is not None
    initial_page = not (show_sender_page or show_recipient_page)
    try:
        recipient_current_page = recipient_paginator.get_page(recipient_page_number)
    except EmptyPage:
        recipient_current_page = recipient_paginator.page(recipient_page_number.num_pages)

    try:
        sender_current_page = sender_paginator.get_page(sender_page_number)
    except EmptyPage:
        sender_current_page = sender_paginator.page(sender_page_number.num_pages)

    # 数据格式处理
    message_list_as_recipient = []
    message_list_as_sender = []
    for obj in recipient_current_page:
        message_list_as_recipient.append({
            "id": obj.id,
            "title": obj.title,
            "from_user_id": obj.from_user.id,
            "from_user_username": obj.from_user.username,
            "read_already": "未读" if obj.read == 0 else "已读",
            "create_time": (obj.create_time + datetime.timedelta(hours=8)).strftime("%m-%d %H:%M"),
            "reply_to": obj.reply_to.id if obj.reply_to else None
        })

    for obj in sender_current_page:
        message_list_as_sender.append({
            "id": obj.id,
            "title": obj.title,
            "to_user_id": obj.to_user.id,
            "to_user_username": obj.to_user.username,
            "read_already": "未读" if obj.read == 0 else "已读",
            "create_time": (obj.create_time + datetime.timedelta(hours=8)).strftime("%m-%d %H:%M"),
            "reply_to": obj.reply_to.id if obj.reply_to else None
        })

    print(message_list_as_sender)

    context = {
        "message_list_as_recipient": message_list_as_recipient,
        "message_list_as_sender": message_list_as_sender,
        "recipient_current_page": recipient_current_page,
        "sender_current_page": sender_current_page,
        "initial_page": initial_page,
        "show_recipient_page": show_recipient_page,
        "show_sender_page": show_sender_page,
    }
    return render(request, "UserMessage/message_list.html", context)


def view_message_detail(request, mid):
    # 获取必要信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo").get("id")).first()
    message_query_set = Message.objects.filter(id=mid)
    if not message_query_set:
        return render(request, "UserAuth/alert_page.html", {"msg": "不存在该条私信"})
    message_obj = message_query_set.first()

    # 检查是否具有阅读权限
    if not (user_obj.id == message_obj.from_user.id or user_obj.id == message_obj.to_user.id):
        return render(request, 'UserAuth/alert_page.html', {"msg": "没有查看权限！"})

    content = markdown(message_obj.content)

    context = {
        'message_id': message_obj.id,
        'title': message_obj.title,
        'content': content,
        'from_user_id': message_obj.from_user.id,
        'to_user_id': message_obj.to_user.id,
        'from_user_username': message_obj.from_user.username,
        'to_user_username': message_obj.to_user.username,
        'create_time': (message_obj.create_time + datetime.timedelta(hours=8)).strftime("%m-%d %H:%M"),
        'can_reply': True if user_obj.id == message_obj.to_user.id else False,
        'reply_to': message_obj.reply_to.id if message_obj.reply_to else None
    }

    # 如果是收件人，则其应该已经阅读过了
    if user_obj.id == message_obj.to_user.id:
        message_query_set.update(read=1)

    return render(request, "UserMessage/message_detail.html", context)
