from django.urls import path
from UserAuth import views


app_name = 'UserAuth'
urlpatterns = [
    path("login/", views.login, name='login'),
    path("register/", views.register, name='register'),
    path("reset/", views.reset_password, name='reset_password'),
    path("changeidentity/", views.change_identity),

    path("gencode/", views.generate_verification_code, name='gencode'),
    path("sendemail/", views.register_email, name='sendemail'),
    path("resetpasswordemail/", views.reset_password_email, name='reset_password_email'),

    path("state/", views.check_login_state),
    path("logout/", views.logout, name='logout'),

]
