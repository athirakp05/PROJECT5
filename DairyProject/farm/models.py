from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError('The Email field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, role='Admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, role=role, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'
    SELLER = 'Seller'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CUSTOMER)
    email = models.EmailField(unique=True)
    
    # Add fields for first name and last name
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    objects = CustomUserManager()
    
    # Define boolean fields for specific roles
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    # Specify a related_name for groups
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set',
        related_query_name='user',
    )

    # Specify a related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username
