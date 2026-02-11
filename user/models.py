from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin , AbstractUser

from .manager import Usermanager


class CustomUser(AbstractUser, PermissionsMixin):
    username =None
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = Usermanager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email