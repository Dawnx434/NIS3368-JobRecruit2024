from django.urls import path

from Application import views

urlpatterns = [
    path('apply/<int:pid>/', views.apply),
    path('cancel/<int:pid>/', views.cancel),
    path('resume/view/<int:uid>/<int:pid>/', views.hr_view_resume),
    path('apply_all/', views.apply_all,name='apply_all')

]