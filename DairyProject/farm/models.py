# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from .custom_models import CustomGroup  # Import your custom models from custom_models.py


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, mobile=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role='Admin', mobile=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role=role, mobile=mobile, **extra_fields)

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
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')

    def __str__(self):
        return self.email

class Society(models.Model):
    district = models.CharField(max_length=20)
    subdistrict = models.CharField(max_length=50)
    panchayath = models.CharField(max_length=50)
    ward_no = models.IntegerField()
    farmer = models.ForeignKey('SellerEditProfile', on_delete=models.CASCADE, related_name='societies')

class IFSCCode(models.Model):
    bankname = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    accno = models.IntegerField()
    farmer = models.ForeignKey('SellerEditProfile', on_delete=models.CASCADE, related_name='ifsccodes')

class SellerEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    house_name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    pin_code = models.IntegerField()
    occupation = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    rationcard_no = models.IntegerField()
    email = models.EmailField()
    mobile = models.CharField(max_length=20, blank=True, null=True)
    acc_no = models.IntegerField()
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='farmers')
    profile_photo = models.ImageField(upload_to='seller_profile_photos/', null=True, blank=True)

    # Add any other fields you need for your Seller model

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)  # Added for Customer's first name
    last_name = models.CharField(max_length=50)  # Added for Customer's last name
    mobile = models.CharField(max_length=20, blank=True, null=True)

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)  # Added for Seller's first name
    last_name = models.CharField(max_length=50)  # Added for Seller's last name
    mobile = models.CharField(max_length=15,blank=True, null=True)

class CustomerEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    dob = models.DateField()
    card_number = models.CharField(max_length=20)
    # Add other customer-specific fields
    profile_photo = models.ImageField(upload_to='Your_Profile/', null=True, blank=True)
