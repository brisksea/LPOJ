# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('wiki', views.WikiView)
routers.register('wikicount', views.WikiCountView)
routers.register('mbcode', views.MBCodeView)
routers.register('mbcodedetail', views.MBCodeDetailView)
routers.register('mbcodedetailnocode', views.MBCodeDetailNoCodeView)
routers.register('trainning', views.TrainningContestView)

urlpatterns = [
    path('', include(routers.urls)),
]
