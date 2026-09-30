"""
Main URL configuration for student_task_manager project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Panel route
    path('admin/', admin.site.urls),

    # Tasks App URLs ko include kar rahe hain root URL ('') par
    path('', include('tasks.urls')),
]
