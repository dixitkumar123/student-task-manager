from django.db import models
from django.contrib.auth.models import User

# Student Task Model - Har task database mein save hoga
class Task(models.Model):
    # Priority ke options define kar rahe hain
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    # Status ke options define kar rahe hain
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    # Har task ek specific student (User) se linked hoga
    # Agar user delete hota hai toh uske saare tasks bhi delete ho jayenge (CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    # Task ka title (max length 200 characters)
    title = models.CharField(max_length=200)

    # Task ki detail description (optional field, khali reh sakta hai)
    description = models.TextField(blank=True, null=True)

    # Priority level: High, Medium, ya Low (default Medium hai)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    # Task completion due date (optional)
    due_date = models.DateField(blank=True, null=True)

    # Task status: Pending ya Completed (default Pending)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    # Task kab bana, auto timestamp ho jayega
    created_at = models.DateTimeField(auto_now_add=True)

    # Django admin ya shell mein display name ke liye __str__ method
    def __str__(self):
        return f"{self.title} ({self.priority}) - {self.user.username}"

    # Default ordering: Naye tasks sabse pehle dikhenge
    class Meta:
        ordering = ['-created_at']
