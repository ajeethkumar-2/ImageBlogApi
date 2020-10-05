from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=252, default='hi')
    last_name = models.CharField(max_length=252, default='user')
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
