from django.urls import path, include
from . import views
from django.urls import re_path as url

urlpatterns = [
    
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/profile/', views.update_profile, name='update'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('search/', views.search_profile, name='search'),
    path('home', views.index, name='landing'),
    path('signup', views.sign_up),
    path('', views.welcome, name='welcome'),
    path('index', views.sign_up, name='index'),
    # path('image/', views.post, name='post'),
    path('like/<id>', views.like_video, name='like'),
    path('video/<id>', views.comment, name='comment'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

  
]


