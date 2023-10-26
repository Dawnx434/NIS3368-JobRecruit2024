from django.urls import path

from UserMessage import views

app_name = "UserMessage"
urlpatterns = [
    path("send/", views.send_message),
    path("list/", views.message_list, name="message_box"),
    path("view/<int:mid>/", views.view_message_detail)
]
