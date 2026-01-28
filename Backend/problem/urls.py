# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('problem', views.ProblemView)
routers.register('problemdata', views.ProblemDataView)
routers.register('problemtag', views.ProblemTagView)
routers.register('choiceproblem', views.ChoiceProblemView)

urlpatterns = [
    path('', include(routers.urls)),
    re_path(r'^uploadfile', views.UploadFileAPIView.as_view()),
    re_path(r'^downloadfile/',views.filedown,name='download'),
    re_path(r'^showpic/',views.showpic,name='show_picture'),
    re_path(r'^judgerdownloadfile/',views.judgerfiledown,name='judgerfiledown'),
    re_path(r'^judgerfiletime/',views.judgerfiletime,name='judgerfiletime'),
]
