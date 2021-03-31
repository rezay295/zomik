from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='panel_index'),
    path('login/', views.login, name='panel_login'),
    path('dashboard/', views.dashboard, name='panel_dashboard'),
    path('add-category/', views.add_catergory, name='panel_add_category'),
    path('list-category/', views.list_catergory, name='panel_list_category'),
    path('add-member/', views.add_member, name='panel_add_member'),
    path('list-member/', views.list_member, name='panel_list_member'),
    path('add-news/', views.add_news, name='panel_add_news'),
    path('list-news/', views.list_news, name='panel_list_news'),
    path('edit-news/<int:news_id>/', views.edit_news, name='panel_edit_news'),

    path('ajax/delete-category/', views.ajax_delete_category, name='panel_ajax_delete_category'),




    path('logout/', views.logout_view, name='panel_logout'),
]