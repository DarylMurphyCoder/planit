from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Model for task categories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Task(models.Model):
    """Model for tasks/todos"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    due_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TaskNote(models.Model):
    """Model for detailed notes on tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.task.title}"


class RecurringTask(models.Model):
    """Model for recurring task patterns"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='recurrence')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.title} - {self.frequency}"


class SharedTaskList(models.Model):
    """Model for sharing tasks with other users"""
    PERMISSION_CHOICES = [
        ('view_only', 'View Only'),
        ('editable', 'Editable'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='shared_with')
    shared_with_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_tasks'
    )
    permission_level = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES,
        default='view_only'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'shared_with_user')

    def __str__(self):
        return f"{self.task.title} shared with {self.shared_with_user.username}"
