from django.urls import path
from UserInfo import views

urlpatterns = [
   path("index/", views.index),
   path("resume/", views.resume),
   path("application/", views.apply),
   path("info/", views.info),
   path("account/",views.account),
   path("logout/",views.logout),
   path("modify/", views.modify),
]
