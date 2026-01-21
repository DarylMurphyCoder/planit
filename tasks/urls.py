from django.urls import path
from .views import (
    task_list, task_detail, task_create, task_update, task_delete, task_toggle,
    category_list, category_create, category_update, category_delete
)

urlpatterns = [
    # Web interface URLs
    path('', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/<int:pk>/edit/', task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task-delete'),
    path('tasks/<int:pk>/toggle/', task_toggle, name='task-toggle'),

    # Category management URLs
    path('categories/', category_list, name='category-list'),
    path('categories/create/', category_create, name='category-create'),
    path('categories/<int:pk>/edit/', category_update, name='category-update'),
    path(
        'categories/<int:pk>/delete/',
        category_delete,
        name='category-delete'
    ),
]
