from django.urls import path
from UserInfo import views
from UserAuth import views as auth_model


app_name = "UserInfo"
urlpatterns = [
   path("index/", views.index, name='index'),
   path("resume/", views.resume, name="resume"),
   path("application/", views.apply, name='application'),
   path("info/", views.info, name='user_info'),
   path("account/",views.account, name='account'),
   path("logout/",auth_model.logout),
   path("modify/", views.modify),
   path("upload/",views.image_upload,name='image_upload'),
   path("resume_upload/",views.resume_upload,name="resume_upload"),
   path("resume_download/", views.resume_download),
   path('show_index/',views.show_index),
]
