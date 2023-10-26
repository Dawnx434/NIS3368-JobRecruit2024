from django.urls import path

from Application import views

urlpatterns = [
    path('apply/<int:pid>/', views.apply),
    path('cancel/<int:pid>/', views.cancel),

]