from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class PublicAuthTests(TestCase):
    def test_public_registration_creates_unverified_user(self):
        response = self.client.post(reverse("register"), {
            "full_name": "Ada Lovelace",
            "email": "ada@example.com",
            "password1": "StrongPass12345",
            "password2": "StrongPass12345",
            "accept_terms": "on",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="ada@example.com")
        self.assertFalse(user.is_email_verified)
