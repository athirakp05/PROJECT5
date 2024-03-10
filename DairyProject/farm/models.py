# models.py

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from .custom_models import CustomGroup

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
    VETERINARIAN='Veterinarian'
    DELIVERY_BOY = 'Delivery Boy'

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
        (ADMIN, 'Admin'),
        (VETERINARIAN, 'Veterinarian'),
        (DELIVERY_BOY , 'Delivery Boy'),

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
    is_veterinarian = models.BooleanField(default=False)
    is_delivery_boy = models.BooleanField(default=False)
    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='custom_user_groups')
    is_active = models.BooleanField(default=True)
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')
    def save(self, *args, **kwargs):
        # Set is_customer, is_seller, or is_admin based on the role
        if self.role == CustomUser.CUSTOMER:
            self.is_customer = True
        elif self.role == CustomUser.SELLER:
            self.is_seller = True
        elif self.role == CustomUser.ADMIN:
            self.is_admin = True
        elif self.role == CustomUser.VETERINARIAN:
            self.is_veterinarian = True    
        elif self.role == CustomUser.DELIVERY_BOY:
            self.is_delivery_boy = True    

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
    pincode = models.IntegerField(null=True, blank=True, default=None)

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
    is_approved = models.BooleanField(default=False)  # Field to track approval status
    is_active = models.BooleanField(default=True)  # Field to track account status

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
    is_active = models.BooleanField(default=True)  # Field to track account status

    def __str__(self):
        return self.first_name
    # Add any other fields you need for your Seller model

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)  # Added for Customer's first name
    last_name = models.CharField(max_length=50)  # Added for Customer's last name
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Field to track account status

    def __str__(self):
        return self.first_name


class CustomerEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,default=True)  # Added for Customer's first name
    last_name = models.CharField(max_length=50,default=True,)  # Added for Customer's last name
    email = models.EmailField(null=False)
    mobile = models.CharField(max_length=20, blank=True, null=False)
    city = models.CharField(max_length=50,null=True)
    dob = models.DateField(null=True)
    card_number = models.CharField(max_length=20,null=True)
    profile_photo = models.ImageField(upload_to='Your_Profile/', null=True, blank=True)
    def __str__(self):
        return self.first_name
class CattleType(models.Model):
    CATTLETYPE_CHOICES = [
        ('cow', 'COW'),
        ('goat', 'GOAT'),
        ('buffalo', 'BUFFALO'),
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Link to the Seller model
    cattle_license = models.CharField(max_length=10,unique=True)  # Field to store farmer license number
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


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # New field to mark message read or unread

    def __str__(self):
        return self.subject
class Veterinarian(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, default=True)
    doctor_name = models.CharField(max_length=50, null=False)
    mobile = models.IntegerField(null=False)
    doctor_license = models.CharField(max_length=10, null=False, unique=True,default=True)  # Update this line
    email = models.EmailField(null=False)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Field to track account status
    specialization = models.CharField(
        max_length=50,
        choices=[
            ('Bovine Practitioner', 'Bovine Practitioner'),
            ('Reproductive Specialist', 'Reproductive Specialist'),
            ('Herd Health Veterinarian', 'Herd Health Veterinarian'),
            ('Cattle Surgery Specialist', 'Cattle Surgery Specialist'),
            ('Food Animal Veterinarian', 'Food Animal Veterinarian'),
            ('Veterinary Epidemiologist', 'Veterinary Epidemiologist'),
            ('Dairy Cattle Veterinarian', 'Dairy Cattle Veterinarian'),
        ],
        null=False,default=True
    )

    def __str__(self):
        return f"Dr. {self.doctor_name} - {self.specialization}"

class VetEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    veterinarian = models.OneToOneField(Veterinarian, on_delete=models.CASCADE)
    house_name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    pin_code = models.IntegerField(null=True, blank=True, default=None)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(null=True, blank=True, default=None)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='vet_profile_photos/', null=True, blank=True)
    doctor_name = models.CharField(max_length=50, null=True)  # Add this line
    doctor_license = models.CharField(max_length=10, null=True)  # Add this line
    specialization = models.CharField(max_length=50, null=True)  # Add this line

    def __str__(self):
        return f"Dr. {self.veterinarian.doctor_name} - {self.veterinarian.specialization}"

# models.py

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    date = models.DateField()
    description = models.TextField(default=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment {self.id} for {self.seller.email} with Dr. {self.veterinarian.doctor_name} on {self.date}"

class DeliveryBoy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    driving_license = models.ImageField(upload_to='driving_license/', null=True, blank=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    is_active = models.BooleanField(default=True)  # Field to track account status
    is_approved = models.BooleanField(default=False)  # Added field for approval status

    def __str__(self):
        return self.first_name
    
class DeliveryBoyEditProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    delivery_boy = models.OneToOneField(DeliveryBoy, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    house_name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    pin_code = models.IntegerField(null=True, blank=True, default=None)
    driving_license = models.CharField(max_length=50, unique=False)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='delivery_boy_profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Field to track account status

    def __str__(self):
        return self.first_name