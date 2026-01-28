# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('ojmessage', views.OJMessageView)
routers.register('blog', views.BlogView)
routers.register('banner', views.BannerView)

urlpatterns = [
    path('', include(routers.urls)),
]
