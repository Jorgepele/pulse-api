"""Tests for the authentication flow: register -> login -> access protected endpoint."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthFlowTests(APITestCase):
    def test_register_creates_user_and_returns_token(self):
        response = self.client.post(
            reverse("register"),
            {"email": "ana@example.com", "password": "s3cure-pass", "full_name": "Ana"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["email"], "ana@example.com")
        self.assertTrue(User.objects.filter(email="ana@example.com").exists())

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse("register"),
            {"email": "weak@example.com", "password": "123"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="weak@example.com").exists())

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(email="dup@example.com", password="s3cure-pass")
        response = self.client.post(
            reverse("register"),
            {"email": "dup@example.com", "password": "another-pass"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_token_for_valid_credentials(self):
        User.objects.create_user(email="ana@example.com", password="s3cure-pass")
        response = self.client.post(
            reverse("login"),
            {"email": "ana@example.com", "password": "s3cure-pass"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_rejects_wrong_password(self):
        User.objects.create_user(email="ana@example.com", password="s3cure-pass")
        response = self.client.post(
            reverse("login"),
            {"email": "ana@example.com", "password": "wrong"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_with_token(self):
        user = User.objects.create_user(email="ana@example.com", password="s3cure-pass")
        login = self.client.post(
            reverse("login"),
            {"email": "ana@example.com", "password": "s3cure-pass"},
        )
        token = login.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
