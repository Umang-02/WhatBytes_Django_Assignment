from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('forget-password',views.ForgetPassword,name='forget-password'),
    path('change-password/<token>',views.changePassword,name='change-password'),
    path('profile',views.profile,name='profile'),
]