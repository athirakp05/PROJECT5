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
        
    
    
    

    # Fields for custom user roles
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CUSTOMER)
    forget_password_token = models.UUIDField(null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    username= None
    phone = models.CharField(max_length=15, null=True, blank=True)
    # Define boolean fields for specific roles (customize these as needed)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Use custom Group model
    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')


    def __str__(self):
        return self.email