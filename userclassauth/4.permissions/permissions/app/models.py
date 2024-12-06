from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    def has_permission(self, permission):
        """Check permission based on role and permissions hierarchy."""
        role_permissions = {
            'guest': [],
            'user': ['view_data'],
            'admin': ['view_data', 'edit_data', 'delete_data'],
        }
        return permission in role_permissions.get(self.role, [])
