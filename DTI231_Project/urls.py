from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('sign-in', views.sign_in, name='sign-in'),  
    path('sign-up', views.signup, name='sign-up'),  
    path('profile', views.profile, name='profile'),  
    path('logout', views.logout_user, name='logout'), 
]

