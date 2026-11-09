# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('board', views.BoardView)
routers.register('dailyboard', views.DailyBoardView)
routers.register('teamboard', views.TeamBoardView)
routers.register('dailycontestboard', views.DailyContestBoardView)
routers.register('settingboard', views.SettingBoardView)

urlpatterns = [
    path('', include(routers.urls)),
]
