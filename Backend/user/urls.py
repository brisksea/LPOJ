# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('userdata', views.UserDataView)
routers.register('user', views.UserView)
#routers.register('change', views.UserChangeView)
#routers.register('changeall', views.UserChangeAllView)
routers.register('userlogindata', views.UserLoginDataView)

urlpatterns = [
    path('', include(routers.urls)),
    re_path(r'^register', views.UserRegisterAPIView.as_view()),
    re_path(r'^login', views.UserLoginAPIView.as_view()),
    re_path(r'^logout', views.UserLogoutAPIView.as_view()),
    re_path(r'^updaterating', views.UserUpdateRatingAPIView.as_view()),
    re_path(r'^setlogindata', views.UserLoginDataAPIView.as_view()),
    re_path(r'^changeone', views.UserChangeView.as_view()),
    re_path(r'^changeall', views.UserChangeAllView.as_view()),
]
