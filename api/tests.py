from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.contrib.auth.models import User
from django.urls import reverse
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
        self.user = User.objects.create(username='test_user', password='test_password', email = "test_email@gmail.com")
        self.user_url = reverse('user-detail', kwargs={'pk': self.user.pk})
    
    def test_get_task(self):
        # creates a ssample task and compare its defailts
        task = Task.objects.create(user=self.user, title='test_title', description='test_description')
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test_title')
        self.assertEqual(response.data['description'], 'test_description')
        self.assertEqual(response.data['user'], self.user.pk)
        
    def test_update_task(self):
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