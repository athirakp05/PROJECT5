from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from .custom_models import CustomGroup
import random
import string   
from django.db import models
from django.contrib.auth.models import User 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, phone=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role='Admin', phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role=role, phone=phone, **extra_fields)

class CustomUser(AbstractUser):
    CUSTOMER = 'Customer'
    SELLER = 'Seller'
    ADMIN = 'Admin'

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CUSTOMER)
    forget_password_token = models.UUIDField(null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    username = None
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Add an email field to the Customer model

    def __str__(self):
        return self.firstname


class Seller(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    # Add other fields as specified
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class SellerEdit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    HouseName = models.CharField(max_length=100)
    City = models.CharField(max_length=50)
    PinCode = models.CharField(max_length=10)
    Occupation = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField()
    RationcardNo = models.CharField(max_length=20)
    Email = models.EmailField()
    Mobile = models.CharField(max_length=15)
    AccNo = models.CharField(max_length=20)
    Societycode = models.CharField(max_length=20)
    Photo = models.ImageField(upload_to='seller_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}'s Seller Edit Profile"
     # You can use the built-in User model or your CustomUser model


class CustomerEdit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)  
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    housename = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    district = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstname} {self.lastname}'s Customer Edit Profile"


