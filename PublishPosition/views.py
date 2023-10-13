from django.shortcuts import render, HttpResponse

from PublishPosition.models import Position

from PublishPosition.utils.provincelist import province_dictionary


# Create your views here.
def position_list(request):
    """返回职位列表"""
    # get query condition: Page and PageSize
    try:
        page = 1 if not request.GET.get('Page') else int(request.GET.get('Page'))
        pagesize = 20 if not request.GET.get('PageSize') else int(request.GET.get('PageSize'))
    except ValueError as e:
        return HttpResponse("异常的查询参数")

    # get list
    query_set = Position.objects.filter(published_state=1)

    # filter according to query params
    query_set = query_set[(page - 1) * pagesize: page * pagesize - 1]

    context = {
        'query_set': query_set

    }
    return render(request, 'PublishPosition/position_list.html', context)


def view_position_detail(request, nid):
    """展示岗位的详细信息"""
    obj = Position.objects.filter(id=nid, published_state=1)  # 1 表示已发布
    # 判空
    if not obj:
        return HttpResponse("不存在的招聘信息或未开放的招聘信息")

    position = obj.first()
    context = {
        "position_name": position.position_name,
        "salary": position.salary,
        "summary": position.summary,
        "detail": position.detail,
        "HR": position.HR,
        "province": position.get_province_display(),
    }

    return render(request, "PublishPosition/position_detail.html", context)


def publish_position(request):
    context = {
        'province_dictionary': province_dictionary
    }
    return render(request, "PublishPosition/position_publish.html", context)
