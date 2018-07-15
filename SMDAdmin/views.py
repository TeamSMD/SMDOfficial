from django.shortcuts import render, HttpResponseRedirect, Http404
from db import smd_admins, artExpo_works  # , artExpo_users


# Create your views here.
def check_if_logged_in(request) -> bool:
    if 'admin_username' in request.session and request.session['username'] != '':
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
                request.session['admin_username'] = request.POST['username']
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
    request.session['admin_username'] = ''
    return HttpResponseRedirect('/smdadmin')


def work_list(request):
    if check_if_logged_in(request):
        works = artExpo_works.list_all_works()
        authors = artExpo_works.list_all_authors()
        for work in works.values():
            work['author_name'] = authors[work['author']]['name']
        return render(request, 'SMDAdmin/works.html', {'works': works})
    else:
        raise Http404


def work_detail(request, work_id):
    if check_if_logged_in(request):
        work = artExpo_works.get_work(work_id)
        author = artExpo_works.get_author(work['author'])
        return render(request, 'SMDAdmin/work_detail.html',
                      {'work_id': work_id,
                       'work_name': work['name'],
                       'author_name': author['name'],
                       'author_id': work['author'],
                       'author_list': artExpo_works.list_all_authors(),
                       'work_description': work['description']})
    else:
        raise Http404


def update_work(request):
    if check_if_logged_in(request):
        if request.method == 'GET':
            return HttpResponseRedirect('/smdadmin')
        elif request.method == 'POST':
            post_data = request.POST
            artExpo_works.update_work(int(post_data['txt_work_id']),
                                      post_data['work_name'],
                                      post_data['txt_author_id'],
                                      post_data['work_description'])
            return HttpResponseRedirect('/smdadmin/work_detail/' + post_data['txt_work_id'] + '/')
    else:
        raise Http404


def add_work(request):
    if check_if_logged_in(request):
        if request.method == 'GET':
            return render(request, 'SMDAdmin/add_work.html', {'author_list': artExpo_works.list_all_authors()})
        elif request.method == 'POST':
            post_data = request.POST
            work_id = artExpo_works.new_art_work(post_data['work_name'],
                                                 post_data['author_id'],
                                                 post_data['work_description'])
            work = artExpo_works.get_work(work_id)
            author = artExpo_works.get_author(work['author'])
            return render(request, 'SMDAdmin/work_detail.html',
                          {'AlertMessage': '添加成功, 作品id: ' + str(work_id),
                           'Back_Url': '/smdadmin/works',
                           'work_id': work_id,
                           'work_name': work['name'],
                           'author_name': author['name'],
                           'author_id': work['author'],
                           'author_list': artExpo_works.list_all_authors(),
                           'work_description': work['description']})
    else:
        raise Http404


def del_work(request, work_id):
    if check_if_logged_in(request):
        artExpo_works.delete_work(work_id)
        return HttpResponseRedirect('/smdadmin/works')
