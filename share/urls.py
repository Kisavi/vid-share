from django.urls import path
from . import views

urlpatterns = [
    
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/profile/', views.update_profile, name='update'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('search/', views.search_profile, name='search'),
  
]


