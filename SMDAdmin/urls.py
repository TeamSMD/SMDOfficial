from django.urls import path
from SMDAdmin import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
]
