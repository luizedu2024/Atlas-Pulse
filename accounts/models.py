from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        ENGINEER = "engineer", "Engineer"
        OPERATOR = "operator", "Operator"
        VIEWER = "viewer", "Viewer"

    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        "organizations.Organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.VIEWER)

    def can_manage(self):
        return self.role == self.Role.ADMIN

    def can_operate(self):
        return self.role in {self.Role.ADMIN, self.Role.ENGINEER, self.Role.OPERATOR}
