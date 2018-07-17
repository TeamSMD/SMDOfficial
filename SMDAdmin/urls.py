from django.urls import path
from SMDAdmin import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('works', views.work_list),
    path('work_detail/<int:work_id>/', views.work_detail),
    path('update_work', views.update_work),
    path('add_work', views.add_work),
    path('del_work/<int:work_id>/', views.del_work),
    path('authors', views.author_list),
    path('author_detail/<int:author_id>/', views.author_detail),
    path('update_author', views.update_author),
    path('add_author', views.add_author)
]
