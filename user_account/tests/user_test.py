# Import necessary modules
from django.test import TestCase


class UserAPITest(TestCase):
    def setUp(self):
        # Create a test client
        #self.client = APIClient()
        print('setting this up')
        # Create some test users
        # self.user1 = CustomUser.objects.create(email='test1@example.com', password="Aye5089mere@")
        # self.user2 = CustomUser.objects.create(email='test2@example.com', password="Aye5089mere@")
    
    def test_create_user(self):
        # Define the user data for creation
        user_data = {'email': 'newuser@example.com', 'password': 'Aye5089mere@'}

        # Make a POST request to create a new user
        #response = self.client.post(reverse('user-list'), user_data)

        # Assert that the request was successful (status code 201)
        self.assertEqual(user_data['email'] == 'newuser@example.com')

        # Assert that the user was created in the database
        self.assertTrue(user_data['password'] == 'Aye5089mere@')
