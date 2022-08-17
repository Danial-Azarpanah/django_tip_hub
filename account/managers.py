from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, phone_number, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            phone_number,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
