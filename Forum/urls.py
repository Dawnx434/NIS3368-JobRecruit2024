from django.urls import path
from Forum import views

app_name = 'Forum'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topics/<int:pk>/', views.topic_posts, name='topic_posts'),
]