from django.urls import path
from UserAuth import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("gencode/", views.generate_verification_code),
    path("state/", views.checkLoginState),
    path("logout/", views.logout),
    path('', views.index),
]
