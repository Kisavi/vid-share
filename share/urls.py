from django.urls import path
from . import views

urlpatterns = [
    
    path('like/<id>', views.like_post, name='like'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/<to_follow>', views.follow, name='follow'),
    
]