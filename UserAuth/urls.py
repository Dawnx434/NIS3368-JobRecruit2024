from django.urls import path
from UserAuth import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("reset/", views.reset_password),

    path("gencode/", views.generate_verification_code),
    path("sendemail/", views.register_email),
    path("resetpasswordemail/", views.reset_password_email),

    path("state/", views.check_login_state),
    path("logout/", views.logout),

]
