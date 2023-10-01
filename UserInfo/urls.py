from django.urls import path
from UserInfo import views

urlpatterns = [
    path("index/", views.index),
    path("resume/", views.resume),
    path("application/", views.apply),
    path("account/", views.account),
    path("modify/", views.modify),
    path("submit/", views.change_sql),
]
