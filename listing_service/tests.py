from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserProfileViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
        # URLs to test
        self.add_property_url = reverse('listing_service:add_property')
        self.login_url = reverse('account_login')
        
    # Test: add property view requires login   
    def test_add_property_view_requires_login(self):
        response = self.client.get(self.add_property_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
    
	# Test: add property view works when logged in 
    def test_add_property_view_when_logged_in(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.add_property_url)
        self.assertEqual(response.status_code, 200) # Success status code
        self.assertTemplateUsed(response, 'listing_service/add_property.html')
            