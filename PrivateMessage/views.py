from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.core.paginator import Paginator, EmptyPage
from django.utils.functional import SimpleLazyObject

import re
import os
from django.conf import settings
from UserAuth.models import User
from django.http import HttpResponse
from django.db.models import Q

# 获取用户头像的帮助函数
def get_matching_files(request):
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


# 收件箱视图
# @login_required
def inbox(request):
    # 获取当前用户的ID
    user_id = request.session['UserInfo'].get('id')
    current_user = User.objects.get(id=user_id)

    # 获取当前用户收到的所有消息和发送的消息
    received_messages = Message.objects.filter(recipient=current_user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=current_user).order_by('-timestamp')

    # 分页功能
    messages_per_page = 10
    paginator = Paginator(received_messages, messages_per_page)
    page_number = request.GET.get('page')

    try:
        current_page = paginator.get_page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'matching_files': get_matching_files(request),  # 用户头像
        'received_messages': current_page,
        'sent_messages': sent_messages,
    }
    return render(request, 'PrivateMessage/inbox.html', context)


# 发送消息视图
# @login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():

            # for user in all_users:
            #     print(f"用户ID: {user.id}, 用户名: {user.username}")

            if isinstance(request.user, SimpleLazyObject):
                # sender = User.objects.get(pk=request.user.id)
                # print(request.session['UserInfo'].get('id'))
                sender = User.objects.get(pk=request.session['UserInfo'].get('id'))
            else:
                sender = request.user
            recipient_id = request.POST.get('recipient')
            recipient = User.objects.get(pk=recipient_id)

            # 获取收件人的ID
            recipient_id = request.POST.get('recipient')

            # 打印发件人和收件人的ID，确保它们是有效的
            print(f"发件人ID: {sender.id}, 收件人ID: {recipient_id}")

            try:
                recipient = User.objects.get(pk=recipient_id)  # 获取收件人
                print(f"收件人信息: {recipient}")
            except User.DoesNotExist:
                return HttpResponse("收件人不存在")

            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()

            return redirect('PrivateMessage:inbox')
    else:
        form = MessageForm()

    users = User.objects.all()

    context = {
        'form': form,
        'users': users,
        'matching_files': get_matching_files(request),
    }
    return render(request, 'PrivateMessage/send_message.html', context)


# 查看消息详情视图
# @login_required

def view_message(request, message_id):
    # 获取当前用户的ID
    user_id = request.session['UserInfo'].get('id')
    current_user = User.objects.get(id=user_id)

    # 使用 Q 对象确保用户可以查看自己作为发件人或收件人的消息
    message = get_object_or_404(Message, Q(id=message_id) & (Q(recipient=current_user) | Q(sender=current_user)))

    message.is_read = True  # 将消息标记为已读
    message.save()

    context = {
        'message': message,
        'matching_files': get_matching_files(request),  # 用户头像
    }
    return render(request, 'PrivateMessage/view_message.html', context)


# @login_required
def reply_message(request, message_id):
    # 获取当前用户的ID
    user_id = request.session['UserInfo'].get('id')
    current_user = User.objects.get(id=user_id)

    # 获取原消息
    original_message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = current_user  # 当前登录用户作为发件人
            reply.recipient = original_message.sender  # 原消息的发件人作为收件人
            reply.save()

            return redirect('PrivateMessage:inbox')  # 回复成功后返回收件箱
    else:
        form = MessageForm()

    context = {
        'form': form,
        'matching_files': get_matching_files(request),  # 用户头像
        'original_message': original_message,  # 显示原消息内容
    }
    return render(request, 'PrivateMessage/reply_message.html', context)