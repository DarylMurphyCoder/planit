"""Test fixtures and utilities for creating test data"""
from django.contrib.auth.models import User
from tasks.models import Task, Category
from datetime import date, timedelta


def create_test_user(username='testuser', password='testpass123', **kwargs):
    """Create a test user with optional additional fields"""
    return User.objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def create_test_category(user, name='Test Category', **kwargs):
    """Create a test category"""
    return Category.objects.create(
        user=user,
        name=name,
        **kwargs
    )


def create_test_task(user, title='Test Task', **kwargs):
    """Create a test task with default values"""
    defaults = {
        'description': 'Test description',
        'priority': 'medium',
        'is_completed': False,
    }
    defaults.update(kwargs)

    return Task.objects.create(
        user=user,
        title=title,
        **defaults
    )


def create_multiple_tasks(user, count=5, **kwargs):
    """Create multiple test tasks"""
    tasks = []
    for i in range(count):
        task = create_test_task(
            user=user,
            title=f'Task {i + 1}',
            **kwargs
        )
        tasks.append(task)
    return tasks


def create_test_data_set(user):
    """Create a complete set of test data for a user"""
    # Create categories
    categories = {
        'work': create_test_category(user, 'Work'),
        'personal': create_test_category(user, 'Personal'),
        'shopping': create_test_category(user, 'Shopping'),
    }
    
    # Create tasks with various attributes
    tasks = {
        'high_priority': create_test_task(
            user=user,
            title='Urgent task',
            priority='high',
            due_date=date.today() + timedelta(days=1),
            category=categories['work']
        ),
        'completed': create_test_task(
            user=user,
            title='Completed task',
            is_completed=True,
            category=categories['personal']
        ),
        'overdue': create_test_task(
            user=user,
            title='Overdue task',
            due_date=date.today() - timedelta(days=2),
            category=categories['work']
        ),
        'no_category': create_test_task(
            user=user,
            title='Task without category',
            priority='low'
        ),
    }
    
    return {
        'categories': categories,
        'tasks': tasks
    }
