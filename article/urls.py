from django.contrib import admin
from django.urls import path, include
from article import views

app_name = 'article'

urlpatterns = [
    path('article_list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
]
