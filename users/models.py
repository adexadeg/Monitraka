from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager




# Create your models here..

Options = (('Whatsapp','Whatsapp'), ('Twitter','Twitter'), ('Instagram','Instagram'), ('A friend','A friend'), ('Our Team','Our Team'))
class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=255, unique= True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, null=True)
    how_did_you_hear_about_us = models.CharField(max_length=300, choices=Options, null=True)
    last_login = models.DateField(null=True)
    is_verified = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='users/profile/avatars', null=True, blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


