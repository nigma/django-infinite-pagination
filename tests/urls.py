#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import ArticleListView

urlpatterns = patterns("",
    url(r"^articles/", ArticleListView.as_view()),
)
