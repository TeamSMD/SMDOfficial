from django.shortcuts import HttpResponse
from django.http import JsonResponse
from db import artExpo_users

# Create your views here.


def index(request):
    return HttpResponse('Team-SMD APIs')


def check_password(request):
    if request.method == 'GET' and 'auth' in request.session and request.session['auth']:
        if 'username' in request.GET and 'password' in request.GET:
            r = artExpo_users.check_password(request.GET['username'], request.GET['password'])
            return JsonResponse({'ok': r})
        else:
            return JsonResponse({'error', 'args missing'})


def get_coins(request):
    if request.method == 'GET' and 'auth' in request.session and request.session['auth']:
        if 'username' in request.GET:
            r = artExpo_users.get_coins(request.GET['username'])
            if r == -1:
                return JsonResponse({'error': 'user not found'})
            else:
                return JsonResponse({'coins': r})


def auth(request):
    if request.method == 'GET':
        if 'password' in request.GET:
            if request.GET['password'] == 'ztudMEGx0CNtTlHj1fVvkS7aJoj9QZN5BP4toSXWwsexNE1iMJXys6jTacrvbz4F':
                request.session['auth'] = True
                return HttpResponse('OK')
            else:
                return HttpResponse('failed')


def add_value(request):
    if request.method == 'GET' and 'auth' in request.session and request.session['auth']:
        if artExpo_users.check_username_availability(request.GET['username']):
            return HttpResponse('User not found')
        else:
            artExpo_users.add_coins(request.GET['username'], request.GET['coins'])
            return HttpResponse('OK')