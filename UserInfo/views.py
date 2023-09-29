from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    name = request.session.get("UserInfo")
    context = {"username": name}
    return render(request, "index.html", context)
def resume(request):
    return 1
def apply(request):
    return 1
def account(request):
    return 1
def logout(request):
    request.session.clear()
    return redirect("/")
def info(request):
    return 1

