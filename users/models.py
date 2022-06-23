from email.policy import default
from select import select
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser

# from user.managers import UserManager
# from .managers import UserManager


# Create your models here..

Options = (('Whatsapp','Whatsapp'), ('Twitter','Twitter'), ('Instagram','Instagram'), ('A friend','A friend'), ('Our Team','Our Team'))
class User(AbstractBaseUser,models.Model):
    fullname = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=255, unique= True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, null=True)
    how_did_you_hear_about_us = models.CharField(max_length=300, choices=Options, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # lastname= models.CharField(max_length=255, blank=True, null=True)
    # image = models.FileField(upload_to='users/', blank=True, null=True)
    
    # last_login = models.DateField(null=True)
    # is_verified = models.BooleanField(null=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    
#     objects = UserManager()



#     def __str__(self):
#         return f'{self.firstname} {self.email}'

#     class Meta:
#         ordering = ('-created_at',)


