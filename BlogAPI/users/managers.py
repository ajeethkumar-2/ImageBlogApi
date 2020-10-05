from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def base_user_create_func(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email is must to create an account.')
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            last_login=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self.base_user_create_func(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self.base_user_create_func(email, password, True, True, **extra_fields)

