# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('putitem', views.ItemPutView)

urlpatterns = [
    path('', include(routers.urls)),
    re_path(r'^item', views.ItemGetAPIView.as_view()),
]
