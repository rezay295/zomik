from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:cat_id>/', views.list_category_news, name='list_category_news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
]