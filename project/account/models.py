from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    This is the overall manager that manages the creation of custom user accounts.
    """
    def _create_user(self, email, username, first_name, last_name, password, **extra_fields):
        values = [email, username, first_name, last_name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
        """Creates and saves the user"""
        extra_fields.setdefault('is_staff', False)  # Makes sure that the new user does not have staff permission 
        extra_fields.setdefault('is_superuser', False)  # Makes sure that the new user does not have superuser permission
        return self._create_user(email, username, first_name, last_name, password, **extra_fields)

    def create_staffuser(self, email, username, fist_name, last_name, password, **extra_fields):
        """Creates and saves the staffuser and determines the permissions it has."""
        extra_fields.setdefault('is_staff', True) # Makes sure that the new staffuser has staff permission
        extra_fields.setdefault('is_superuser', False) # Makes sure that the new staffuser does not have superuser permission

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        return self._create_user(email, username, fist_name, last_name, password, **extra_fields)

    def create_superuser(self, email, username, fist_name, last_name, password, **extra_fields):
        """Creates and saves the superuser and makes sure it has all the permissions."""
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, fist_name, last_name, password, **extra_fields)

class Account(AbstractBaseUser):
    """
    This is class that contains the new custom fields in the custom user model
    """
    email = models.EmailField(verbose_name='email address', max_length=60, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=40, unique=True)
    last_name = models.CharField(verbose_name='last name', max_length=40, unique=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

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
