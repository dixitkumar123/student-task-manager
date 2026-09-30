from django.urls import path
from . import views

# Tasks app ke URL patterns
urlpatterns = [
    # Task List (Dashboard) - Home page for logged-in user
    path('', views.task_list, name='task_list'),

    # Task CRUD URLs
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:task_id>/edit/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:task_id>/toggle/', views.task_toggle_status, name='task_toggle_status'),

    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
