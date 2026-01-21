from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Task, Category, TaskNote, RecurringTask, SharedTaskList


class TaskModelTest(TestCase):
    """Test cases for the Task model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category'
        )
    
    def test_task_creation(self):
        """Test creating a task with all fields"""
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test description',
            priority='high',
            due_date=date.today() + timedelta(days=7),
            category=self.category
        )
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test description')
        self.assertEqual(task.priority, 'high')
        self.assertFalse(task.is_completed)
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.category, self.category)
    
    def test_task_optional_fields(self):
        """Test creating task with only required fields"""
        task = Task.objects.create(
            user=self.user,
            title='Minimal Task'
        )
        
        self.assertEqual(task.title, 'Minimal Task')
        self.assertIsNone(task.description)
        self.assertEqual(task.priority, 'medium')  # default
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.category)
        self.assertFalse(task.is_completed)
    
    def test_task_string_representation(self):
        """Test task __str__ method"""
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_priority_choices(self):
        """Test all priority levels"""
        priorities = ['low', 'medium', 'high']
        for priority in priorities:
            task = Task.objects.create(
                user=self.user,
                title=f'{priority} priority task',
                priority=priority
            )
            self.assertEqual(task.priority, priority)


class CategoryModelTest(TestCase):
    """Test cases for the Category model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(
            user=self.user,
            name='Work'
        )
        
        self.assertEqual(category.name, 'Work')
        self.assertEqual(category.user, self.user)
    
    def test_category_string_representation(self):
        """Test category __str__ method"""
        category = Category.objects.create(
            user=self.user,
            name='Personal'
        )
        self.assertEqual(str(category), 'Personal')
    
    def test_category_with_tasks(self):
        """Test category with related tasks"""
        category = Category.objects.create(
            user=self.user,
            name='Project'
        )
        
        task1 = Task.objects.create(
            user=self.user,
            title='Task 1',
            category=category
        )
        task2 = Task.objects.create(
            user=self.user,
            title='Task 2',
            category=category
        )
        
        self.assertEqual(category.tasks.count(), 2)
        self.assertIn(task1, category.tasks.all())
        self.assertIn(task2, category.tasks.all())


class TaskViewTest(TestCase):
    """Test cases for task views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_task_list_view_requires_login(self):
        """Test that task list requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_task_list_view_authenticated(self):
        """Test task list view for authenticated user"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
    
    def test_task_list_view_context_data(self):
        """Test context data in task list view"""
        Task.objects.create(
            user=self.user,
            title='Task 1',
            is_completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Task 2',
            is_completed=True
        )
        
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.context['total_tasks'], 2)
        self.assertEqual(response.context['pending_tasks'], 1)
        self.assertEqual(response.context['completed_tasks'], 1)
    
    def test_task_list_filter_by_status(self):
        """Test filtering tasks by completion status"""
        Task.objects.create(
            user=self.user,
            title='Pending Task',
            is_completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Completed Task',
            is_completed=True
        )
        
        # Filter for pending tasks
        response = self.client.get(reverse('task-list') + '?status=pending')
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Pending Task')
        
        # Filter for completed tasks
        response = self.client.get(reverse('task-list') + '?status=completed')
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Completed Task')
    
    def test_task_list_filter_by_priority(self):
        """Test filtering tasks by priority"""
        Task.objects.create(
            user=self.user,
            title='High Priority',
            priority='high'
        )
        Task.objects.create(
            user=self.user,
            title='Low Priority',
            priority='low'
        )
        
        response = self.client.get(reverse('task-list') + '?priority=high')
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, 'high')
    
    def test_task_list_search(self):
        """Test searching tasks by title"""
        Task.objects.create(user=self.user, title='Buy groceries')
        Task.objects.create(user=self.user, title='Pay bills')
        
        response = self.client.get(reverse('task-list') + '?search=groceries')
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Buy groceries')
    
    def test_task_detail_view(self):
        """Test task detail view"""
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test description'
        )
        
        response = self.client.get(reverse('task-detail', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], task)
    
    def test_task_detail_view_other_user_task(self):
        """Test accessing another user's task returns 404"""
        other_task = Task.objects.create(
            user=self.other_user,
            title='Other User Task'
        )
        
        response = self.client.get(
            reverse('task-detail', args=[other_task.pk])
        )
        self.assertEqual(response.status_code, 404)
    
    def test_task_create_view_get(self):
        """Test GET request to create task view"""
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
    
    def test_task_create_view_post(self):
        """Test POST request to create a task"""
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'priority': 'high',
            'due_date': '2026-12-31',
            'category': self.category.pk
        }
        
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        task = Task.objects.get(title='New Task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.description, 'Task description')
        self.assertEqual(task.priority, 'high')
    
    def test_task_update_view_post(self):
        """Test updating a task"""
        task = Task.objects.create(
            user=self.user,
            title='Original Title',
            priority='low'
        )
        
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'priority': 'high'
        }
        
        response = self.client.post(
            reverse('task-update', args=[task.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
        self.assertEqual(task.priority, 'high')
    
    def test_task_delete_view(self):
        """Test deleting a task"""
        task = Task.objects.create(
            user=self.user,
            title='Task to Delete'
        )
        
        response = self.client.post(reverse('task-delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=task.pk)
    
    def test_task_toggle_view(self):
        """Test toggling task completion status"""
        task = Task.objects.create(
            user=self.user,
            title='Task to Toggle',
            is_completed=False
        )
        
        response = self.client.post(reverse('task-toggle', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        
        # Toggle again
        response = self.client.post(reverse('task-toggle', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertFalse(task.is_completed)


class CategoryViewTest(TestCase):
    """Test cases for category views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_category_list_view(self):
        """Test category list view"""
        Category.objects.create(user=self.user, name='Work')
        Category.objects.create(user=self.user, name='Personal')
        
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/category_list.html')
        self.assertEqual(len(response.context['categories']), 2)
    
    def test_category_create_view_post(self):
        """Test creating a category"""
        data = {'name': 'Shopping'}
        
        response = self.client.post(reverse('category-create'), data)
        self.assertEqual(response.status_code, 302)
        
        category = Category.objects.get(name='Shopping')
        self.assertEqual(category.user, self.user)
    
    def test_category_create_duplicate_name(self):
        """Test creating duplicate category name"""
        Category.objects.create(user=self.user, name='Work')
        
        data = {'name': 'Work'}
        self.client.post(reverse('category-create'), data)
        
        # Should still have only one 'Work' category
        self.assertEqual(Category.objects.filter(name='Work').count(), 1)
    
    def test_category_update_view(self):
        """Test updating a category"""
        category = Category.objects.create(user=self.user, name='Old Name')
        
        data = {'name': 'New Name'}
        response = self.client.post(
            reverse('category-update', args=[category.pk]),
            data
        )
        
        category.refresh_from_db()
        self.assertEqual(category.name, 'New Name')
    
    def test_category_delete_view(self):
        """Test deleting a category"""
        category = Category.objects.create(user=self.user, name='To Delete')
        
        # Create task with this category
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            category=category
        )
        
        self.client.post(reverse('category-delete', args=[category.pk]))
        
        # Category should be deleted
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=category.pk)
        
        # Task should still exist but with no category
        task.refresh_from_db()
        self.assertIsNone(task.category)


class TaskNoteModelTest(TestCase):
    """Test cases for TaskNote model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
    
    def test_task_note_creation(self):
        """Test creating a task note"""
        note = TaskNote.objects.create(
            task=self.task,
            content='This is a note'
        )
        
        self.assertEqual(note.task, self.task)
        self.assertEqual(note.content, 'This is a note')
    
    def test_task_note_string_representation(self):
        """Test task note __str__ method"""
        note = TaskNote.objects.create(
            task=self.task,
            content='Test note'
        )
        self.assertEqual(str(note), f'Note for {self.task.title}')


class RecurringTaskModelTest(TestCase):
    """Test cases for RecurringTask model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Recurring Task'
        )
    
    def test_recurring_task_creation(self):
        """Test creating a recurring task"""
        recurring = RecurringTask.objects.create(
            task=self.task,
            frequency='weekly',
            end_date=date.today() + timedelta(days=30)
        )
        
        self.assertEqual(recurring.task, self.task)
        self.assertEqual(recurring.frequency, 'weekly')
    
    def test_recurring_task_frequencies(self):
        """Test all frequency options"""
        frequencies = ['daily', 'weekly', 'monthly', 'yearly']
        
        for freq in frequencies:
            task = Task.objects.create(
                user=self.user,
                title=f'{freq} task'
            )
            recurring = RecurringTask.objects.create(
                task=task,
                frequency=freq
            )
            self.assertEqual(recurring.frequency, freq)


class SharedTaskListModelTest(TestCase):
    """Test cases for SharedTaskList model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.task = Task.objects.create(
            user=self.user1,
            title='Shared Task'
        )
    
    def test_shared_task_creation(self):
        """Test sharing a task with another user"""
        shared = SharedTaskList.objects.create(
            task=self.task,
            shared_with_user=self.user2,
            permission_level='view_only'
        )
        
        self.assertEqual(shared.task, self.task)
        self.assertEqual(shared.shared_with_user, self.user2)
        self.assertEqual(shared.permission_level, 'view_only')
    
    def test_shared_task_permissions(self):
        """Test different permission levels"""
        permissions = ['view_only', 'editable']
        
        for perm in permissions:
            user = User.objects.create_user(
                username=f'user_{perm}',
                password='pass123'
            )
            shared = SharedTaskList.objects.create(
                task=self.task,
                shared_with_user=user,
                permission_level=perm
            )
            self.assertEqual(shared.permission_level, perm)
