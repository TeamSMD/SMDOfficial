from django.urls import path
from SMDAdmin import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('works', views.work_list),
    path('work_detail/<int:work_id>/', views.work_detail)
]
