from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.

class UserTestCases(APITestCase):
    def setUp(self):
        #use teardown here to ensure db is clear
        self.tearDown()
        # create a user and get the url for the user
        self.user = User.objects.create(username='test_user', password='test_password', email='test_email@gmail.com')
        self.user_url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def tearDown(self):
        # sued to clear the user data after each test
        User.objects.all().delete()

    def test_create_user(self):
        # creates a additional user and see if its created
        url = reverse('user-list')
        data = {
            'username': 'test_user2',
            'email': 'test_email2@gmail.com',
            'password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
    
    def test_get_user(self):
        # gets the base user details and check if its correct
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_update_user(self):
        # test update using patch, put should work the same way, except it requires all fields
        data = {
            'username': 'updated_user',
            'email': 'updated_email@gmail.com'
        }
        response = self.client.patch(self.user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])

    def test_delete_user(self):
        # deletes the user and check if it was deleted
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class TaskTestCases(APITestCase):
    # will suppress the create test, since im using it every other test
    
    def tearDown(self):
        User.objects.all().delete()
        Task.objects.all().delete()

    def setUp(self):
        #use teardown here to ensure db is clear
        self.tearDown()
        # create a user and get the url for the user
        self.user = User.objects.create_user(username='test_user', password='test_password', email='test_email@gmail.com')
        self.client.login(username='test_user', password='test_password')
        self.task_url = reverse('task-list')

        #get the tokens and put access token str on access
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)
    
    def test_task_authenticated(self):
        # creates a task and check if it was created
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        data = {
            "title": "test_title",
            "description": "test_description"
        }
        response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_task_unauthenticated(self):
        # removes the token and check if it works
        data = {
            "title": "test_title",
            "description": "test_description"
        }
        response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_update_authenticated(self):
        # need to clean up this test later, maybe do a single task creation at setUp
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        data = {
            "title": "test_title",
            "description": "test_description"
        }
        creation_response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(creation_response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title='test_title')
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {
            "title": "test_title_moded",
        }
        response = self.client.patch(task_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
    
    def test_task_delete_authenticated(self):
        # also need some clean up here
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        data = {
            "title": "test_title",
            "description": "test_description"
        }
        creation_response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(creation_response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title='test_title')
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



'''    def test_update_task(self):
        # creates a sample task and updates its status
        task = Task.objects.create(user=self.user, title='test_title', description='test_description')
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {
            "title": "updated_title",
            "description": "updated_description",
            "completed": True
        }
        response = self.client.patch(task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['completed'], data['completed'])

    def test_delete_task(self):
        # creates a sample task and deletes it
        task = Task.objects.create(user=self.user, title='test_title', description='test_description')
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
'''