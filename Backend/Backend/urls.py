"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('problem.urls')),
    path('', include('judgestatus.urls')),
    path('', include('user.urls')),
    path('', include('contest.urls')),
    path('', include('board.urls')),
    path('', include('blog.urls')),
    path('', include('wiki.urls')),
    path('', include('item.urls')),
    path('', include('classes.urls')),
]
