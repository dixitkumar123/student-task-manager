from django.contrib import admin
from .models import Task

# Task model ko Django Admin Panel mein register kar rahe hain
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Admin table mein display hone wale columns
    list_display = ('title', 'user', 'priority', 'status', 'due_date', 'created_at')

    # Filtering options on admin sidebar
    list_filter = ('status', 'priority', 'created_at')

    # Search bar options
    search_fields = ('title', 'description', 'user__username')
