from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        # ("guest", "Guest"),
        ("patron", "Patron"),
        ("librarian", "Librarian"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patron")

    profile_image = models.URLField(blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )
