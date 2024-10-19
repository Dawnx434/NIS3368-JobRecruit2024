from django.urls import path
from . import views

app_name = "PrivateMessage"

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),  # 收件箱
    path('send_message/', views.send_message, name='send_message'),  # 发送消息
    path('message/<int:message_id>/', views.view_message, name='view_message'),  # 查看单条消息
]