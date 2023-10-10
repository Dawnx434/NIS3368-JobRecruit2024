from django.urls import path
from UserInfo import views
from UserAuth import views as auth_model
urlpatterns = [
   path("index/", views.index),
   path("resume/", views.resume),
   path("application/", views.apply),
   path("info/", views.info),
   path("account/",views.account),
   path("logout/",auth_model.logout),
   path("modify/", views.modify),
   path("upload/",views.image_upload,name='image_upload'),
   path("resume_upload/",views.resume_upload,name="resume_upload"),
]
