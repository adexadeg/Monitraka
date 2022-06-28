from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from .managers import UserManager

# from user.managers import UserManager
# from .managers import UserManager


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



#     def __str__(self):
#         return f'{self.firstname} {self.email}'

#     class Meta:
#         ordering = ('-created_at',)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


