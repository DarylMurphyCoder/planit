from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet, CategoryViewSet,
    task_list, task_detail, task_create, task_update, task_delete, task_toggle
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Web interface URLs
    path('', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/<int:pk>/edit/', task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task-delete'),
    path('tasks/<int:pk>/toggle/', task_toggle, name='task-toggle'),
    
    # API URLs
    path('api/', include(router.urls)),
]
