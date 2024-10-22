from django.urls import path
from . import views

app_name = "PrivateMessage"

urlpatterns = [
    # path('inbox/', views.inbox, name='inbox'),  # 收件箱
    # path('send_message/', views.send_message, name='send_message'),  # 发送消息
    # path('message/<int:message_id>/', views.view_message, name='view_message'),  # 查看单条消息
    path('', views.conversation_view, name='conversation'),  # 修改为空前缀
    path('<int:selected_user_id>/', views.conversation_view, name='conversation'),
    # path('<int:selected_user_id>/', views.conversation_view, name='conversation_with_user'),  # 特定用户对话
    path('send/', views.send_message, name='send_message'),
]