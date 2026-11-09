# -*- coding: utf-8 -*-
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('contestannouncement', views.ContestAnnouncementView)
routers.register('contestcomment', views.ContestCommentView)
routers.register('contestinfo', views.ContestInfoView)
routers.register('contestcominginfo', views.ContestComingInfoView)
routers.register('contestproblem', views.ContestProblemView)
routers.register('contestboard', views.ContestBoardView)
routers.register('contestregister', views.ContestRegisterView)
routers.register('contestratingchange', views.ContestRatingChangeView)
routers.register('contesttutorial', views.ContestTutorialView)
routers.register('contesttotalboard', views.ContestBoardTotalView)
routers.register('conteststudentchoiceanswer', views.StudentChoiceAnswerView)
routers.register('contestchoiceproblem', views.ContestChoiceProblemView)

urlpatterns = [
    path('', include(routers.urls)),
    re_path(r'^currenttime', views.CurrentTimeView.as_view()),
    re_path(r'^contestfilterboard', views.ContestBoardFilterAPIView.as_view()),
    re_path(r'^getcontestchoiceproblems', views.GetContestChoiceProblems.as_view()),
    re_path(r'^scorecontestchoiceproblems', views.ScoreContestChoiceProblems.as_view()),
    re_path(r'^isboardlock', views.ContestIsBoardLockAPIView.as_view()),

]
