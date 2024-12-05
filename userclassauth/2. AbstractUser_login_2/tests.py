from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

class UserViewsTestCase(TestCase):

    def setUp(self):
        """Set up a user for testing."""
        self.client = Client()
        self.username = 'testuser'
        self.password = 'Password123!'
        self.email = 'testuser@example.com'
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_home_page_logged_in(self):
        """Test that the home page is accessible when logged in."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TODO-APP')  # Adjust this if necessary

    def test_home_page_not_logged_in(self):
        """Test that the home page redirects if not logged in."""
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_register_user_valid_data(self):
        """Test registration with valid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))

        # Check if user was created
        user = get_user_model().objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_user_invalid_data(self):
        """Test registration with invalid data (password mismatch)."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPassword123!',
            'password2': 'InvalidPassword123',
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        # Adjust this if the form has a different name or structure
        form = response.context['form']
        self.assertTrue(form.errors)  # Check that the form has errors
        self.assertIn('password2', form.errors)  # Ensure the password2 field has an error

    def test_login_user_valid_data(self):
        """Test login with valid data."""
        response = self.client.post(reverse('login'), {
            'username_or_email': self.username,
            'password1': self.password,
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))

    def test_login_user_invalid_data(self):
        """Test login with invalid data."""
        response = self.client.post(reverse('login'), {
            'username_or_email': self.username,
            'password1': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertContains(response, "ERROR: invalid username or password, please check the login details and try again.")

    def test_logout_user(self):
        """Test that the user is logged out."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_register_user_redirect_if_authenticated(self):
        """Test that a logged-in user cannot access the registration page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('home'))

    def test_login_user_redirect_if_authenticated(self):
        """Test that a logged-in user cannot access the login page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_logout_redirect_if_not_authenticated(self):
        """Test that an unauthenticated user is redirected when trying to log out."""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
