from django.shortcuts import render, HttpResponseRedirect
from db import smd_admins


# Create your views here.
def index(request):
    # return render(request, 'SMDAdmin_login.html')
    if 'username' in request.session and request.session['username'] != '':
        return render(request, 'SMDAdmin_Console.html')
    else:
        return HttpResponseRedirect('/smdadmin/login')


def login(request):
    if request.method == "GET":
        if 'username' in request.session and request.session['username'] != "":
            return HttpResponseRedirect('/smdadmin/')
        else:
            return render(request, 'SMDAdmin_login.html')
    elif request.method == "POST":
        if smd_admins.check_password(request.POST['username'], request.POST['password']):
            if smd_admins.check_login_attempt(request.POST['username']):
                request.session['username'] = request.POST['username']
                smd_admins.clear_fail_attempt(request.POST['username'])
                return HttpResponseRedirect('/smdadmin')
            else:
                return render(request, 'SMDAdmin_login.html', {'AlertMessage': '登录失败次数过多'})
        else:
            smd_admins.add_fail_attempt(request.POST['username'])
            if smd_admins.check_login_attempt(request.POST['username']):
                return render(request, 'SMDAdmin_login.html', {'AlertMessage': '用户名密码错误'})
            else:
                return render(request, 'SMDAdmin_login.html', {'AlertMessage': '登录失败次数过多'})


def logout(request):
    request.session['username'] = ''
    return HttpResponseRedirect('/smdadmin')
