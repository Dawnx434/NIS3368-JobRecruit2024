from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.core.paginator import Paginator, EmptyPage

import re
import os
from django.conf import settings

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
@login_required
def inbox(request):
    # 获取当前用户收到的所有消息
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')

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
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # 当前用户作为发送者
            message.save()
            return redirect('PrivateMessage:inbox')  # 跳转回收件箱
    else:
        form = MessageForm()

    context = {
        'form': form,
        'matching_files': get_matching_files(request),  # 用户头像
    }
    return render(request, 'PrivateMessage/send_message.html', context)


# 查看消息详情视图
@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()

    context = {
        'message': message,
        'matching_files': get_matching_files(request),  # 用户头像
    }
    return render(request, 'PrivateMessage/view_message.html', context)