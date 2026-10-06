"""
App1_accounts models: User and AuthorityProfile.

Design notes matching the class diagram:
- No `role` field on User. Whether someone is an authority is decided
  purely by whether an AuthorityProfile row exists for their user_id
  (see User.is_authority below) -- see the diagram note on AuthorityProfile.
- User.area is a nullable FK to reports.Area, added so status/verification
  notifications can be sent to "everyone in this area", not just the
  reporter. Referenced as a string ("reports.Area") to avoid a circular
  import between the accounts and reports apps.
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager: users log in with email, not a separate username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """App1_accounts.User from the class diagram."""

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    area = models.ForeignKey(
        "reports.Area",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="residents",
        help_text="User's home/registered area, used for area-based notifications.",
    )

    trust_score = models.IntegerField(default=50)
    verified_reports = models.PositiveIntegerField(default=0)
    false_reports = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Django admin access, unrelated to AuthorityProfile
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def is_authority(self):
        """True if this user has a linked AuthorityProfile row."""
        return hasattr(self, "authorityprofile")

    def calculate_trust_score(self):
        """Recompute trust_score from verified_reports vs false_reports."""
        total = self.verified_reports + self.false_reports
        if total == 0:
            self.trust_score = 50  # neutral starting score, no history yet
        else:
            self.trust_score = round((self.verified_reports / total) * 100)
        self.save(update_fields=["trust_score"])
        return self.trust_score


class AuthorityProfile(models.Model):
    """App1_accounts.AuthorityProfile -- 1:0..1 extension of User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    area = models.ForeignKey(
        "reports.Area",
        on_delete=models.SET_NULL,
        null=True,
        related_name="authorities",
        help_text="The area this authority is responsible for.",
    )

    def __str__(self):
        return f"{self.user.name} ({self.department})"
