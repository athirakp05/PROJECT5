# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from .custom_models import CustomGroup  # Import your custom models from custom_models.py
from django.core.validators import RegexValidator


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
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    forget_password_token = models.UUIDField(null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = CustomUserManager()
    username = None
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')
    def save(self, *args, **kwargs):
        # Set is_customer, is_seller, or is_admin based on the role
        if self.role == CustomUser.CUSTOMER:
            self.is_customer = True
        elif self.role == CustomUser.SELLER:
            self.is_seller = True
        elif self.role == CustomUser.ADMIN:
            self.is_admin = True

        super().save(*args, **kwargs)
    def __str__(self):
        return self.email
        
class Login_Details(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # You may want to use a more secure field like PasswordField
    role = models.CharField(max_length=15, choices=CustomUser.ROLE_CHOICES)

    def __str__(self):
        return self.email

class Society(models.Model):
    society_code = models.CharField(max_length=20, default='')
    district = models.CharField(max_length=20,default='')
    subdistrict = models.CharField(max_length=50,default='')
    location = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.society_code

class IFSCCode(models.Model):
    bankname = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    ifsccode = models.CharField(max_length=50,default=False)
    def __str__(self):
        return self.ifsccode
class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)  # Added for Seller's first name
    last_name = models.CharField(max_length=50)  # Added for Seller's last name
    mobile = models.CharField(max_length=15,blank=True, null=True)
    farmer_license = models.CharField(max_length=20, unique=True)  # Add 'unique=True'
    def __str__(self):
        return self.first_name
class SellerEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    house_name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    pin_code = models.IntegerField(null=True, blank=True, default=None)
    occupation = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True)
    rationcard_no = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    acc_no = models.IntegerField(null=True)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='farmers', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='seller_profile_photos/', null=True, blank=True)
    farmer_license = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.first_name
    # Add any other fields you need for your Seller model

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)  # Added for Customer's first name
    last_name = models.CharField(max_length=50)  # Added for Customer's last name
    mobile = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.first_name




class CustomerEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    dob = models.DateField()
    card_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='Your_Profile/', null=True, blank=True)

class CattleType(models.Model):
    CATTLETYPE_CHOICES = [
        ('Cow', 'COW'),
        ('Goat', 'GOAT'),
        ('Guffalo', 'BUFFALO'),
    ]
    name = models.CharField(max_length=50, unique=True, primary_key=True,choices=CATTLETYPE_CHOICES,default='')
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")
    def __str__(self):
        return self.name
        
class Breed(models.Model):
    cattle_type = models.ForeignKey(CattleType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")

    def __str__(self):
        return self.name


class Cattle(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,default=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Link to the Seller model
    cattle_license = models.CharField(max_length=10,default=False,unique=True)  # Field to store farmer license number
    EarTagID = models.IntegerField()
    CattleType = models.ForeignKey(CattleType, on_delete=models.CASCADE)
    BreedName = models.ForeignKey(Breed, on_delete=models.CASCADE)
    weight = models.IntegerField()
    height = models.IntegerField()
    Age = models.IntegerField()
    Colour = models.CharField(max_length=50)
    feed = models.CharField(max_length=50)
    milk_obtained = models.IntegerField()
    vaccination = models.BooleanField(default=False)
    insurance = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='cattle_photos/', null=True, blank=True)

    def __str__(self):
        return self.cattle_license

class Insurance(models.Model):
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='insurances')
    INSURANCE_CHOICES = [
        ('Agriculture Insurance Company of India (AIC)', 'Agriculture Insurance Company of India (AIC)'),
        ('National Insurance Company', 'National Insurance Company'),
        ('United India Insurance Company', 'United India Insurance Company'),
        ('HDFC ERGO', 'HDFC ERGO'),
        ('ICICI Lombard', 'ICICI Lombard'),
        ('Bajaj Allianz', 'Bajaj Allianz'),

    ]
    provider_name = models.CharField(max_length=100,unique=True,choices=INSURANCE_CHOICES,default='')
    policy_number = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact_info = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.policy_number

class Vaccination(models.Model):
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='vaccinations')
    VACCINATION_CHOICES = [
        ('Clostridial vaccines', 'Clostridial vaccines'),
        ('Brucellosis vaccine', 'Brucellosis vaccine'),
        ('Caseous lymphadenitis (CL) vaccine', 'Caseous lymphadenitis (CL) vaccine'),
        ('Rinderpest vaccine', 'Rinderpest vaccine'),
        ('Foot and mouth disease (FMD vaccine)', 'Foot and mouth disease (FMD) vaccine'),

    ]
    vaccine_name = models.CharField(max_length=50, unique=True,choices=VACCINATION_CHOICES,default='')
    date_administered = models.DateField()
    next_due_date = models.DateField()
    administered_by = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.vaccine_name
        



