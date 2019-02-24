from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserAPITest(TestCase):
    ''' Test the users api public '''
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        ''' Test creating a user with a valid payload is successful '''
        payload = {
            'email': 'testapp@gmail.com',
            'password': 'testpass',
            'name': 'testap',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        ''' Test creating a user that already exists should fails '''
        payload = {
            'email': 'test_2@gmail.com',
            'password': 'test_2_222',
            'name': 'test_2',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        ''' Test that the password must be more than 5 characters '''
        payload = {
            'email': 'test_3@gmail.com',
            'password': 'pas',
            'name': 'test_3'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        ''' Test that a token is created for a user '''
        payload = {
            'email': 'testtoken@gmail.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        ''' Test that the token is not created if invalid credentials are given '''
        create_user(email='user_test@gmail.com', password='abc1233')
        payload = {
            'email': 'user_test@gmail.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        ''' Test that token is not created if the user not exists '''
        payload = {
            'email': 'user_test@gmail.com',
            'password': 'testpassword',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_password_field(self):
        ''' Test that token is not created if the password is not given '''
        res = self.client.post(TOKEN_URL, {'email': 'test@gmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_email_field(self):
        res = self.client.post(TOKEN_URL, {'email': '', 'password': '123test'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
