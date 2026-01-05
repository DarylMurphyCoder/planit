from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Category


# Template-based views for web interface
@login_required
def task_list(request):
    """Display list of tasks with filtering"""
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters
    if status_filter == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(is_completed=False)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)
    
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    
    # Calculate stats
    total_tasks = Task.objects.filter(user=request.user).count()
    pending_tasks = Task.objects.filter(user=request.user, is_completed=False).count()
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()
    
    context = {
        'tasks': tasks.order_by('-created_at'),
        'categories': categories,
        'status': status_filter,
        'priority': priority_filter,
        'category': category_filter,
        'search': search_query,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    """Display task details"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    """Create a new task"""
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        category_id = request.POST.get('category') or None
        
        task = Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id
        )
        
        messages.success(request, f'Task "{task.title}" created successfully!')
        return redirect('task-list')
    
    context = {
        'categories': categories,
        'form_title': 'Create New Task',
        'form': {},
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, pk):
    """Update an existing task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority', 'medium')
        task.due_date = request.POST.get('due_date') or None
        task.category_id = request.POST.get('category') or None
        task.is_completed = 'is_completed' in request.POST
        task.save()
        
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect('task-detail', pk=task.pk)
    
    context = {
        'task': task,
        'categories': categories,
        'form_title': 'Edit Task',
        'form': {
            'title': {'value': task.title},
            'description': {'value': task.description},
            'priority': {'value': task.priority},
            'due_date': {'value': task.due_date},
            'category': {'value': task.category_id if task.category else ''},
            'is_completed': {'value': task.is_completed},
        }
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_delete(request, pk):
    """Delete a task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect('task-list')
    
    return redirect('task-detail', pk=pk)


@login_required
def task_toggle(request, pk):
    """Toggle task completion status"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
        
        status_msg = 'completed' if task.is_completed else 'marked as pending'
        messages.success(request, f'Task "{task.title}" {status_msg}!')
    
    # Redirect back to the referring page or task list
    return redirect(request.META.get('HTTP_REFERER', 'task-list'))
