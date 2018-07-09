from django.shortcuts import render, HttpResponseRedirect
from db import smd_admins


# Create your views here.
def check_if_logged_in(request)->bool:
    if 'username' in request.session and request.session['username'] != '':
        return True
    else:
        return False


def index(request):
    # return render(request, 'login.html')
    if check_if_logged_in(request):
        return render(request, 'SMDAdmin/Console.html')
    else:
        return HttpResponseRedirect('/smdadmin/login')


def login(request):
    if request.method == "GET":
        if check_if_logged_in(request):
            return HttpResponseRedirect('/smdadmin/')
        else:
            return render(request, 'SMDAdmin/login.html')
    elif request.method == "POST":
        if smd_admins.check_password(request.POST['username'], request.POST['password']):
            if smd_admins.check_login_attempt(request.POST['username']):
                request.session['username'] = request.POST['username']
                smd_admins.clear_fail_attempt(request.POST['username'])
                return HttpResponseRedirect('/smdadmin')
            else:
                return render(request, 'SMDAdmin/login.html', {'AlertMessage': '登录失败次数过多'})
        elif smd_admins.user_exists(request.POST['username']):
            return render(request, 'SMDAdmin/login.html', {'AlertMessage': '用户名密码错误'})
        else:
            smd_admins.add_fail_attempt(request.POST['username'])
            if smd_admins.check_login_attempt(request.POST['username']):
                return render(request, 'SMDAdmin/login.html', {'AlertMessage': '用户名密码错误'})
            else:
                return render(request, 'SMDAdmin/login.html', {'AlertMessage': '登录失败次数过多'})


def logout(request):
    request.session['username'] = ''
    return HttpResponseRedirect('/smdadmin')


def work_list(request):
    pass