from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the custom NewUser model below
    """

    def create_superuser(self, email, username, first_name, last_name, password,
                         **other_fields):
        # Set is_staff, is_superuser, and is_active to True as default
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email=email, username=username, first_name=first_name, last_name=last_name,
                                password=password,
                                **other_fields)

    def create_user(self, email, username, first_name=None, last_name=None, password=None,
                    **other_fields):
        # Check if user has entered an email
        if not email:
            raise ValueError('You must provide an email address')

        # Set the values to the variables for creating a user account
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user
