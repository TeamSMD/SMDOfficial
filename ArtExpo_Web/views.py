from django.shortcuts import render, Http404, HttpResponseRedirect
from django.http import JsonResponse
from db import artExpo_works, artExpo_users

# Create your views here.

ARTEXPO_MODE = 1


def index(request):
    print(request.META['HTTP_USER_AGENT'])
    if 'username' in request.session:
        return render(request, 'ArtExpo_Index.html', {'username': request.session['username'], 'mode': ARTEXPO_MODE})
    else:
        return render(request, 'ArtExpo_Index.html', {'mode': ARTEXPO_MODE})


def Works(request, workNo):
    work_info = artExpo_works.get_work(workNo)
    if 'error' in work_info:
        raise Http404
    else:
        author_name = artExpo_works.get_author(work_info['author'])['name']
        return render(request, 'works.html', {'work_name': work_info['name'], 'work_id': workNo,
                                              'author_name': author_name, 'author_id': work_info['author'],
                                              'work_des': work_info['description']})


def Author(request, authorNo):
    author_info = artExpo_works.get_author(authorNo)
    if 'error' in author_info:
        raise Http404
    else:
        return render(request, 'author.html', {'author_name': author_info['name'],
                                               'description': author_info['description'],
                                               'author_id': authorNo})


def login(request):
    if request.method == 'POST':
        if artExpo_users.check_password(request.POST['username'], request.POST['password']):
            request.session['username'] = request.POST['username']
            if 'cont' in request.session and request.session['cont'] != '':
                cont = request.session['cont']
                request.session['cont'] = ''
                return HttpResponseRedirect(cont)
            else:
                return HttpResponseRedirect('/artexpo')
        else:
            return render(request, 'artExpo_Login.html', {'AlertMessage': '用户名或密码错误'})
    elif request.method == "GET":
        if 'username' not in request.session or request.session['username'] == '':
            return render(request, 'artExpo_Login.html')
        else:
            return HttpResponseRedirect('/artexpo')


def register(request):
    if request.method == "POST":
        if artExpo_users.check_username_availability(request.POST['username']):
            artExpo_users.add_user(request.POST['username'], request.POST['password'], '')
            return render(request, 'artExpo_Reg_Success.html')
        else:
            return render(request, 'artExpo_Register.html', {'AlertMessage': '用户名已被占用'})
    elif request.method == "GET":
        return render(request, 'artExpo_Register.html')


def reward(request, workNo):
    if request.method == "POST":
        if int(request.POST['coins']) <= 0:
            return render(request, 'reward_bullshit.html', {'work_id': workNo})
        if artExpo_users.get_coins(request.session['username']) >= int(request.POST['coins']):
            artExpo_works.add_coin(workNo, int(request.POST['coins']))
            artExpo_users.use_coins(request.session['username'], request.POST['coins'])
            return render(request, 'reward_success.html',
                          {'coins_left': artExpo_users.get_coins(request.session['username']),
                           'work_id': workNo})
        else:
            return render(request, 'reward_failed.html', {'work_id': workNo,
                                                          'coins_left': artExpo_users.get_coins
                                                          (request.session['username'])})
    else:
        if 'username' not in request.session or request.session['username'] == '':
            request.session['cont'] = '/artexpo/reward/' + str(workNo) + '/'
            return render(request, 'artExpo_Login.html', {'AlertMessage': '还没有登录哦'})
        work_info = artExpo_works.get_work(workNo)
        if 'error' in work_info:
            raise Http404
        else:
            author_name = artExpo_works.get_author(work_info['author'])['name']
            return render(request, 'reward.html', {'work_name': work_info['name'], 'work_id': workNo,
                                                   'author_name': author_name, 'author_id': work_info['author'],
                                                   'work_des': work_info['description']})


def logout(request):
    request.session['username'] = ''
    return HttpResponseRedirect('/artexpo')


def api_check_username(request):
    if request.method == 'GET':
        r = artExpo_users.check_username_availability(request.GET['username'])
        if r:
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False})
    else:
        raise Http404


def reg_success(request):
    return render(request, 'artExpo_Reg_Success.html')
