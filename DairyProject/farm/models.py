from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from .custom_models import CustomGroup  # Import your custom models from custom_models.py

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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer")
    firstname = models.CharField(max_length=30, default='')
    lastname = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')  # Provide a default value
    phone = models.CharField(max_length=15, default='')  # Provide a default value
    # Add additional fields specific to customers

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seller")
    firstname = models.CharField(max_length=30, default='')
    lastname = models.CharField(max_length=30, default='')
    email = models.EmailField()  # Remove the default value
    phone = models.CharField(max_length=15, default='')  # Provide a default value if needed
    # Add any other additional fields specific to sellers
