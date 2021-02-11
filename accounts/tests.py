from django.test import TestCase
from rest_framework import status
from accounts.models import User
from django.contrib.auth import authenticate


class UserCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@example.com',
                                             password='12test21')

    def test_create_user(self):
        response = self.client.post("/api/auth/register", {
            'email': 'test15@example.com',
            'username': 'test',
            'password': '12test21', })
        user = User.objects.get(email='test15@example.com')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.username, 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_with_existing_email(self):
        response = self.client.post("/api/auth/register", {
            'username': 'test',
            'email': 'test@example.com',
            'password': '', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_invalid_email(self):
        response = self.client.post("/api/auth/register", {
            'username': 'test',
            'email': 'test',
            'password': '', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_email(self):
        response = self.client.post("/api/auth/register", {
            'username': 'test',
            'email': '',
            'password': '12test21', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_password(self):
        response = self.client.post("/api/auth/register", {
            'username': 'test',
            'email': 'test2@example.com',
            'password': '', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_username(self):
        response = self.client.post("/api/auth/register", {
            'username': '',
            'email': 'test3@example.com',
            'password': '12test21', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_empty_user(self):
        response = self.client.post("/api/auth/register", {
            'username': '',
            'email': '',
            'password': '', })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='user@example.com',
                                             password='12test21')
        self.superuser = User.objects.create_superuser(username='test',
                                                       email='superuser@example.com',
                                                       password='12test21')

    def test_login_user(self):
        self.user = authenticate(email='user@example.com', password='12test21')
        self.assertTrue((self.user is not None) and self.user.is_authenticated)

    def test_wrong_email(self):
        self.user = authenticate(email='wrong', password='12test21')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_wrong_password(self):
        self.user = authenticate(email='user@example.com', password='wrong')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_wrong_password_and_email(self):
        self.user = authenticate(email='wrong', password='wrong')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_without_password(self):
        self.user = authenticate(email='user@example.com', password='')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_without_email(self):
        self.user = authenticate(email='', password='12test21')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_empty_user(self):
        self.user = authenticate(email='', password='')
        self.assertFalse((self.user is not None) and self.user.is_authenticated)

    def test_login_superuser(self):
        self.superuser = authenticate(email='superuser@example.com', password='12test21')
        self.assertTrue((self.superuser is not None) and self.superuser.is_authenticated
                        and self.superuser.is_staff and self.superuser.is_superuser)

    def test_check_user_for_superuser(self):
        self.user = authenticate(email='user@example.com', password='12test21')
        self.assertFalse((self.user is not None) and self.user.is_authenticated
                         and self.user.is_staff and self.user.is_superuser)
