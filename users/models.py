from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_customer = False
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(
    #     verbose_name='email',
    #     max_length=255,
    #     unique=True,
    # )
    # is_customer = models.BooleanField(default=True)
    # name = models.CharField(max_length=64, verbose_name='name')

    username = models.CharField(max_length=64)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f'Profile:' \
               f'\n\tEmail: {self.email}' \
               f'\n\tName: {self.username}' \
               f'\n\tIs customer: {self.is_staff}'
