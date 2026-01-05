from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task


class Notification(models.Model):
    """Model for tracking email notifications"""
    NOTIFICATION_TYPES = [
        ('due_soon', 'Due Soon'),
        ('overdue', 'Overdue'),
        ('shared', 'Task Shared'),
        ('completed', 'Task Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} notification for {self.task.title}"
