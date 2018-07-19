

from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('auth', views.auth),
    path('check_password', views.check_password),
    path('get_coins', views.get_coins),
    path('check_user_exists', views.check_user_exists)
]
