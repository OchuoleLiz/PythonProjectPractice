from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        """
        Creates and saves a user with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email, username and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    This is class that contains the custom fields in the custom user model
    """
    email = models.EmailField(verbose_name='email address', max_length=40, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=40, unique=True)
    last_name = models.CharField(verbose_name='last name', max_length=40, unique=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'  # This is the primary identifier being defined for the user
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # The required fields for a new user to sign up

    objects = UserManager()

    def get_full_name(self):
        """Returns the first_name and the last_name"""
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """A short name identifier for the user"""
        return self.username

    def __str__(self):
        """The returns the main identifier for the user"""
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_admin
