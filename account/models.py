from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

import rest_framework.authentication
import rest_framework.authtoken.models


class User(AbstractBaseUser):
    is_client = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = None
    last_login = None

    USERNAME_FIELD = 'id'

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        db_table = 'user'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, default=None)
    gender = models.CharField(max_length=1, choices=settings.GENDERS, null=True, default=None, db_index=True)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, default='ru', db_index=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'
        db_table = 'client'


class Waiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, null=True, default=None)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, default='ru', db_index=True)

    class Meta:
        verbose_name = 'Waiter'
        verbose_name_plural = 'Waiter'
        db_table = 'waiter'


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, null=True, default=None)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, default='ru', db_index=True)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admin'
        db_table = 'admin'


class Token(rest_framework.authtoken.models.Token):
    pass

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Token'
        db_table = 'token'


class TokenAuthentication(rest_framework.authentication.TokenAuthentication):
    model = Token
