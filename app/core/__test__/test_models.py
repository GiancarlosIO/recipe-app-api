from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_sample_user(email='test@gmail.com', password='testpassword'):
    '''Create a sample user model'''
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        ''' Create an user with email is successful '''
        email = 'test@gmail.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        ''' test the email for a new user is normalized '''
        email = 'test@CREHANA.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        ''' Test creating user with no email raises an error '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        ''' creating new superuser '''
        user = get_user_model().objects.create_superuser(
            'giancarlos@crehana.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Vegan',
        )
        self.assertEqual(str(tag), tag.name)
