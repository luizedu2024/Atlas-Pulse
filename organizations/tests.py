from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from organizations.models import Organization, OrganizationMembership


class OrganizationIsolationTests(TestCase):
    def test_create_organization_adds_admin_membership(self):
        user = User.objects.create_user(email="owner@example.com", password="StrongPass12345", full_name="Owner", is_email_verified=True)
        self.client.force_login(user)
        response = self.client.post(reverse("organization_create"), {
            "name": "ACME Industrial",
            "slug": "acme",
            "description": "Tenant",
            "timezone": "UTC",
        })
        self.assertEqual(response.status_code, 302)
        org = Organization.objects.get(slug="acme")
        self.assertTrue(OrganizationMembership.objects.filter(user=user, organization=org, role="admin").exists())
