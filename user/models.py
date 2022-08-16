from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the custom NewUser model below
    """

    def create_superuser(self, email, user_name, first_name, password,
                         **other_fields):

        # Set is_staff, is_superuser, and is_active to True as default
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Check if is_staff and is_superuser are True else raise a ValueError
        if not other_fields.get('is_staff'):
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if not other_fields.get('is_superuser'):
            raise ValueError(
                'Superuser must be assigned to is_superuser=True')

        return self.create_user(email, user_name, first_name, password,
                                **other_fields)

    def create_user(self, email, user_name, first_name, password,
                    **other_fields):

        # Check if user has entered an email
        if not email:
            raise ValueError(_('You must provide an email address'))

        # Set the values to the variables for creating a user account
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Personalized User model with additional fields
    """
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now())
    about = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name
