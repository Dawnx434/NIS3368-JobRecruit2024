from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.core.paginator import Paginator, EmptyPage
from django.utils.functional import SimpleLazyObject
from django.urls import reverse
from django.utils import timezone

import re
import os
from django.conf import settings
from UserAuth.models import User
from django.http import HttpResponse
from django.db.models import Q, Count, Max
from django.http import JsonResponse

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
            sender = User.objects.get(pk=request.session['UserInfo'].get('id'))
            recipient_id = request.POST.get('recipient')
            recipient = User.objects.get(pk=recipient_id)

            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()

            # 发送消息后重定向回当前对话
            return redirect(reverse('PrivateMessage:conversation', args=[recipient.id]))
            # return render(request, 'PrivateMessage/conversation.html')
    else:
        form = MessageForm()

    users = User.objects.all()

    context = {
        'form': form,
        'users': users,
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

# @login_required
from .forms import MessageForm
from django.shortcuts import redirect

# @login_required
from django.utils import timezone

def conversation_view(request, current_user_id, selected_user_id):
    # 获取当前登录用户对象
    current_user = get_object_or_404(User, id=current_user_id)
    selected_user = get_object_or_404(User, id=selected_user_id)

    # 标记与选中联系人的所有未读消息为已读
    Message.objects.filter(sender=selected_user, recipient=current_user, is_read=False).update(is_read=True)

    # 获取与当前登录用户有过互动的联系人列表
    contact_users = User.objects.filter(
        Q(sent_messages__recipient=current_user) | Q(received_messages__sender=current_user)
    ).annotate(
        last_message_time=Max('sent_messages__timestamp', filter=Q(sent_messages__recipient=current_user))
    ).order_by('-last_message_time')

    # 获取每个联系人的未读消息数量
    contact_users = contact_users.annotate(
        unread_count=Count('sent_messages', filter=Q(sent_messages__recipient=current_user, sent_messages__is_read=False))
    )

    # 获取当前登录用户与选中联系人的所有消息
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(recipient=selected_user)) |
        (Q(sender=selected_user) & Q(recipient=current_user))
    ).order_by('timestamp')

    # 格式化消息中的时间戳为东八区
    for message in messages:
        message.timestamp = timezone.localtime(message.timestamp, timezone.get_fixed_timezone(480)).strftime('%Y-%m-%d %H:%M:%S')

    # 消息发送表单
    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = current_user
        message.recipient = selected_user
        message.save()
        # 重新加载页面，避免表单重复提交
        return redirect('PrivateMessage:conversation_with_user', current_user_id=current_user.id, selected_user_id=selected_user.id)

    # 渲染模板
    return render(request, 'PrivateMessage/conversation.html', {
        'contact_users': contact_users,  # 所有联系人
        'messages': messages,  # 消息记录
        'selected_user': selected_user,  # 当前选中联系人
        'current_user': current_user,  # 当前登录用户
        'form': form,  # 消息表单
    })

def fetch_new_messages(request, current_user_id, selected_user_id):
    current_user = get_object_or_404(User, id=current_user_id)
    selected_user = get_object_or_404(User, id=selected_user_id)

    # 获取当前用户和选中的用户之间的所有消息
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(recipient=selected_user)) |
        (Q(sender=selected_user) & Q(recipient=current_user))
    ).order_by('timestamp')

    # 强制将时间转换为东八区格式，避免轮询时发生时区问题
    message_data = [
        {
            'sender_id': message.sender.id,
            'content': message.content,
            'timestamp': timezone.localtime(message.timestamp, timezone.get_fixed_timezone(480)).strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]

    # 返回JSON响应
    return JsonResponse({'messages': message_data})