from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from tasks.models import Category


class SignupViewTest(TestCase):
    """Test cases for user signup functionality"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
    
    def test_signup_view_get(self):
        """Test GET request to signup page"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)
    
    def test_signup_view_post_success(self):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        
        response = self.client.post(self.signup_url, data)
        
        # Should redirect to task list after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        
        # User should be created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # User should be logged in
        user = User.objects.get(username='newuser')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
    
    def test_signup_creates_default_categories(self):
        """Test that default categories are created on signup"""
        data = {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        
        self.client.post(self.signup_url, data)
        
        user = User.objects.get(username='testuser')
        categories = Category.objects.filter(user=user)
        
        # Should have 3 default categories
        self.assertEqual(categories.count(), 3)
        
        # Check category names
        category_names = [cat.name for cat in categories]
        self.assertIn('Home', category_names)
        self.assertIn('Work', category_names)
        self.assertIn('Personal', category_names)
    
    def test_signup_view_post_weak_password(self):
        """Test signup with weak password"""
        data = {
            'username': 'testuser',
            'password1': '123',
            'password2': '123'
        }
        
        response = self.client.post(self.signup_url, data)
        
        # Should stay on signup page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('password2', response.context['form'].errors)
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='testuser').exists())
    
    def test_signup_view_post_password_mismatch(self):
        """Test signup with mismatched passwords"""
        data = {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!'
        }
        
        response = self.client.post(self.signup_url, data)
        
        # Should stay on signup page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('password2', response.context['form'].errors)
    
    def test_signup_view_post_duplicate_username(self):
        """Test signup with existing username"""
        # Create existing user
        User.objects.create_user(username='existinguser', password='pass123')
        
        data = {
            'username': 'existinguser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        
        response = self.client.post(self.signup_url, data)
        
        # Should stay on signup page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('username', response.context['form'].errors)
    
    def test_signup_view_authenticated_user_redirect(self):
        """Test that authenticated users are redirected from signup"""
        User.objects.create_user(username='testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')
        
        response = self.client.get(self.signup_url)
        
        # Should redirect to task list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))


class LoginViewTest(TestCase):
    """Test cases for user login functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('login')
    
    def test_login_view_get(self):
        """Test GET request to login page"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        
        # User should be logged in
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            self.user.pk
        )
    
    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data)
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # User should not be logged in
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_login_view_post_nonexistent_user(self):
        """Test login with non-existent user"""
        data = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        
        response = self.client.post(self.login_url, data)
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # User should not be logged in
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_logout_functionality(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        self.assertIn('_auth_user_id', self.client.session)
        
        # Logout
        response = self.client.post(reverse('logout'))
        
        # Should redirect after logout
        self.assertEqual(response.status_code, 302)
        
        # User should be logged out
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_login_required_redirect(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('task-list'))
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class UserAuthenticationIntegrationTest(TestCase):
    """Integration tests for authentication flow"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_signup_login_logout_flow(self):
        """Test complete authentication workflow"""
        # 1. Signup
        signup_data = {
            'username': 'flowuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)
        
        # User should be logged in after signup
        self.assertIn('_auth_user_id', self.client.session)
        
        # 2. Access protected page
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
        
        # 4. Try to access protected page (should redirect)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)
        
        # 5. Login again
        login_data = {
            'username': 'flowuser',
            'password': 'ComplexPass123!'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        
        # 6. Access protected page again (should work)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
