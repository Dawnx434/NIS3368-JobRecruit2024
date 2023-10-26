from django.urls import path

from UserMessage import views

urlpatterns = [
    path("send/", views.send_message),
]
