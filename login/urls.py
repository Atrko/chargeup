from django.contrib import admin
from django.urls import path
from . import views
#from .views import CreatePostView # new



urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('profile/<int:user_id>', views.profile),
    path('logout', views.logout),
    path('update/<int:user_id>', views.update),
    path('update_photo/', views.update_photo),
    #path('update_photo/', ProfilePageView.as_view(), name='profile'),
    #path('post/', CreatePostView.as_view(), name='update_photo'), # new

]