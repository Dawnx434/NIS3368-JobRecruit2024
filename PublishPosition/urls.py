from django.urls import path

from PublishPosition import views

"""
should include:
/list   展示列表
view/<int: nid>/    查看编号为nid的岗位详情
publish/    发布职位
"""

app_name = "PublishPosition"
urlpatterns = [
    path("list/", views.position_list),
    path("view/<int:nid>/", views.view_position_detail),
    path("publish/", views.publish_position, name='publish'),
    path("modify/<int:nid>/", views.modify_position),
]
