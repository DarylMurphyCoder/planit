"""Integration tests for complete workflows"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from tasks.models import Task, Category


class TaskManagementIntegrationTest(TestCase):
    """End-to-end integration tests for task management"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_complete_task_workflow(self):
        """Test complete task CRUD workflow"""
        # 1. Create a category
        category_data = {'name': 'Project'}
        response = self.client.post(reverse('category-create'), category_data)
        self.assertEqual(response.status_code, 302)
        
        category = Category.objects.get(name='Project')
        
        # 2. Create a task
        task_data = {
            'title': 'Complete project',
            'description': 'Finish the important project',
            'priority': 'high',
            'due_date': (date.today() + timedelta(days=7)).isoformat(),
            'category': category.pk
        }
        response = self.client.post(reverse('task-create'), task_data)
        self.assertEqual(response.status_code, 302)
        
        task = Task.objects.get(title='Complete project')
        self.assertEqual(task.priority, 'high')
        self.assertEqual(task.category, category)
        
        # 3. View task detail
        response = self.client.get(reverse('task-detail', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Complete project')
        
        # 4. Update the task
        update_data = {
            'title': 'Complete important project',
            'description': 'Updated description',
            'priority': 'high',
            'category': category.pk
        }
        response = self.client.post(
            reverse('task-update', args=[task.pk]),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'Complete important project')
        self.assertEqual(task.description, 'Updated description')
        
        # 5. Toggle task completion
        response = self.client.post(reverse('task-toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        
        # 6. Toggle back to pending
        response = self.client.post(reverse('task-toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertFalse(task.is_completed)
        
        # 7. Delete the task
        response = self.client.post(reverse('task-delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
    
    def test_task_filtering_workflow(self):
        """Test filtering and searching tasks"""
        category1 = Category.objects.create(user=self.user, name='Work')
        category2 = Category.objects.create(user=self.user, name='Personal')
        
        # Create tasks with different attributes
        Task.objects.create(
            user=self.user,
            title='Work task 1',
            priority='high',
            is_completed=False,
            category=category1
        )
        Task.objects.create(
            user=self.user,
            title='Work task 2',
            priority='low',
            is_completed=True,
            category=category1
        )
        Task.objects.create(
            user=self.user,
            title='Personal task',
            priority='medium',
            is_completed=False,
            category=category2
        )
        
        # Test filter by status
        response = self.client.get(reverse('task-list') + '?status=pending')
        self.assertEqual(len(response.context['tasks']), 2)
        
        response = self.client.get(reverse('task-list') + '?status=completed')
        self.assertEqual(len(response.context['tasks']), 1)
        
        # Test filter by priority
        response = self.client.get(reverse('task-list') + '?priority=high')
        self.assertEqual(len(response.context['tasks']), 1)
        
        # Test filter by category
        response = self.client.get(
            reverse('task-list') + f'?category={category1.pk}'
        )
        self.assertEqual(len(response.context['tasks']), 2)
        
        # Test search
        response = self.client.get(reverse('task-list') + '?search=Personal')
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].title, 'Personal task')
    
    def test_multi_user_isolation(self):
        """Test that users can only see their own data"""
        # Create second user
        user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        # Create tasks for both users
        task1 = Task.objects.create(
            user=self.user,
            title='User 1 Task'
        )
        task2 = Task.objects.create(
            user=user2,
            title='User 2 Task'
        )
        
        # User 1 should only see their task
        response = self.client.get(reverse('task-list'))
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'User 1 Task')
        
        # User 1 shouldn't be able to access User 2's task
        response = self.client.get(reverse('task-detail', args=[task2.pk]))
        self.assertEqual(response.status_code, 404)
        
        # Login as user 2
        self.client.logout()
        self.client.login(username='user2', password='pass123')
        
        # User 2 should only see their task
        response = self.client.get(reverse('task-list'))
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'User 2 Task')
        
        # User 2 shouldn't be able to access User 1's task
        response = self.client.get(reverse('task-detail', args=[task1.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_category_management_workflow(self):
        """Test complete category management workflow"""
        # Create category
        response = self.client.post(
            reverse('category-create'),
            {'name': 'Shopping'}
        )
        self.assertEqual(response.status_code, 302)
        
        category = Category.objects.get(name='Shopping')
        
        # Create tasks in this category
        Task.objects.create(
            user=self.user,
            title='Buy milk',
            category=category
        )
        Task.objects.create(
            user=self.user,
            title='Buy bread',
            category=category
        )
        
        # View category list
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        categories = response.context['categories']
        shopping_cat = [c for c in categories if c.name == 'Shopping'][0]
        self.assertEqual(shopping_cat.task_count, 2)
        
        # Update category
        response = self.client.post(
            reverse('category-update', args=[category.pk]),
            {'name': 'Groceries'}
        )
        category.refresh_from_db()
        self.assertEqual(category.name, 'Groceries')
        
        # Delete category
        response = self.client.post(
            reverse('category-delete', args=[category.pk])
        )
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())
        
        # Tasks should still exist but without category
        tasks = Task.objects.filter(user=self.user)
        self.assertEqual(tasks.count(), 2)
        for task in tasks:
            self.assertIsNone(task.category)
    
    def test_signup_to_task_creation_flow(self):
        """Test new user flow from signup to creating first task"""
        self.client.logout()
        
        # 1. Signup
        signup_data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='newuser')
        
        # 2. Check default categories were created
        categories = Category.objects.filter(user=user)
        self.assertEqual(categories.count(), 3)
        
        # 3. Create first task using default category
        work_category = Category.objects.get(user=user, name='Work')
        task_data = {
            'title': 'First task',
            'description': 'My first task',
            'priority': 'high',
            'category': work_category.pk
        }
        response = self.client.post(reverse('task-create'), task_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify task was created
        task = Task.objects.get(user=user, title='First task')
        self.assertEqual(task.category, work_category)
        self.assertEqual(task.priority, 'high')
        
        # 5. View task list
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_tasks'], 1)
        self.assertEqual(response.context['pending_tasks'], 1)
        self.assertEqual(response.context['completed_tasks'], 0)


class URLRoutingTest(TestCase):
    """Test URL routing and accessibility"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_public_urls_accessible(self):
        """Test that public URLs are accessible without login"""
        public_urls = [
            reverse('login'),
            reverse('signup'),
        ]
        
        for url in public_urls:
            response = self.client.get(url)
            self.assertIn(
                response.status_code,
                [200, 302],
                f"URL {url} should be accessible"
            )
    
    def test_protected_urls_require_login(self):
        """Test that protected URLs redirect to login"""
        task = Task.objects.create(user=self.user, title='Test Task')
        
        protected_urls = [
            reverse('task-list'),
            reverse('task-create'),
            reverse('task-detail', args=[task.pk]),
            reverse('task-update', args=[task.pk]),
            reverse('category-list'),
            reverse('category-create'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                302,
                f"URL {url} should redirect unauthenticated users"
            )
            self.assertIn('/login/', response.url)
    
    def test_protected_urls_accessible_when_logged_in(self):
        """Test that protected URLs work when logged in"""
        self.client.login(username='testuser', password='testpass123')
        
        category = Category.objects.create(user=self.user, name='Test')
        task = Task.objects.create(user=self.user, title='Test Task')
        
        protected_urls = [
            reverse('task-list'),
            reverse('task-create'),
            reverse('task-detail', args=[task.pk]),
            reverse('task-update', args=[task.pk]),
            reverse('category-list'),
            reverse('category-create'),
            reverse('category-update', args=[category.pk]),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                f"URL {url} should be accessible when logged in"
            )
