

from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('work/<int:workNo>/', views.Works),
    path('author/<int:authorNo>/', views.Author),
    path('register', views.register),
    path('api/checkusername', views.api_check_username),
    path('reward/<int:workNo>/', views.reward),
    path('logout', views.logout)
]
