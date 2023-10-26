from django.shortcuts import render


# Create your views here.
def send_message(request):
    """发送私信"""
    if request.method == "GET":
        return render(request, "UserMessage/send_message.html")
