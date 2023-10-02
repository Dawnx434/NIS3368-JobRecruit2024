from django.shortcuts import render, redirect
from UserAuth.models import User

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
def modify(request):
    context = get_info(request)
    return render(request,"userinfo_modify.html",context)
def change_sql():
    return 1
def logout(request):
    request.session.clear()
    return redirect("/")
def info(request):
    if request.method == 'POST':
        name = request.session.get('UserInfo')
        username = request.POST.get('username')
        mobile_phone = request.POST.get('mobile_phone')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        edu_ground = request.POST.get('edu_ground')
        school = request.POST.get('school')
        major = request.POST.get('major')
        excepting_position = request.POST.get('excepting_position')
        excepting_location = request.POST.get('excepting_location')
        context = {"username": username,
               "id": name['id'],
               "mobile_phone": mobile_phone,
               "gender": gender,
               "email": email,
               "edu_ground": edu_ground,
               "school": school,
               "major": major,
               "excepting_position": excepting_position,
               "excepting_location": excepting_location,
        }
        save(context)
    else:
        context = get_info(request)
    return render(request, "userinfo.html", context)
def get_info(request):
    name = request.session.get("UserInfo")
    mobile_phone = User.objects.get(id=name['id']).mobile_phone
    gender = User.objects.get(id=name['id']).gender
    email = User.objects.get(id=name['id']).email
    edu_ground = User.objects.get(id=name['id']).edu_ground
    school = User.objects.get(id=name['id']).school
    major = User.objects.get(id=name['id']).major
    excepting_position = User.objects.get(id=name['id']).excepting_position
    excepting_location = User.objects.get(id=name['id']).excepting_location
    context = {"username": name['username'],
               "id": name['id'],
               "mobile_phone": mobile_phone,
               "gender": gender,
               "email": email,
               "edu_ground": edu_ground,
               "school": school,
               "major": major,
               "excepting_position": excepting_position,
               "excepting_location": excepting_location,
               }
    return context
def save(context):
    User.objects.get(id=context['id']).username = context.get('username')
    User.objects.get(id=context['id']).mobile_phone = context.get('mobile_phone')
    User.objects.get(id=context['id']).gender = context.get('gender')
    User.objects.get(id=context['id']).email = context.get('email')
    User.objects.get(id=context['id']).edu_ground = context.get('edu_ground')
    User.objects.get(id=context['id']).school = context.get('school')
    User.objects.get(id=context['id']).major = context.get('major')
    User.objects.get(id=context['id']).excepting_position = context.get('excepting_position')
    User.objects.get(id=context['id']).excepting_location = context.get('excepting_location')