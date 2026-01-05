from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks for the current user only"""
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a task"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed tasks for the user"""
        tasks = self.get_queryset().filter(is_completed=True)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending tasks for the user"""
        tasks = self.get_queryset().filter(is_completed=False)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        """Toggle the completion status of a task"""
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return categories for the current user only"""
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a category"""
        serializer.save(user=self.request.user)
