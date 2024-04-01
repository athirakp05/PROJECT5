from django.db import models
from farm.models import Seller,CustomUser
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

class Product(models.Model):
    p_code = models.AutoField(primary_key=True, unique=True)
    p_name = models.CharField(max_length=50, null=False)
    mfg_date = models.DateField()
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    description = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    upload_datetime=models.DateTimeField(default=timezone.now)
    CATEGORY_CHOICES = [
    ('Milk', 'Milk'),
    ('Curd', 'Curd'),
    ('Paneer', 'Paneer'),
    ('Ghee', 'Ghee'),
    ('Butter', 'Butter'),
    ('Cheese', 'Cheese'),
]
    categories = models.CharField(max_length=10, choices=CATEGORY_CHOICES,default='milk')
    image = models.ImageField(upload_to='products/', null=True, blank=True, unique=True)

    def __str__(self):
        return self.p_name

class MilkCollection(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    CATTLE_CHOICES = [
        ('Cow', 'Cow'),
        ('Buffalo', 'Buffalo'),
        ('Goat', 'Goat'),
        # Add more cattle types as needed
    ]
    milk_type = models.CharField(max_length=10, choices=CATTLE_CHOICES, default='Cow')
    collection_date = models.DateField()
    COLLECTION_CHOICES = [
        ('1', 'ForeNoon'),
        ('2', 'AfterNoon'),
]
    collection_time = models.CharField(max_length=50,  choices=COLLECTION_CHOICES,default='1.027-1.03')
    quantity = models.PositiveIntegerField()
    DENSITY_CHOICES = [
        ('density-level above 1.03', 'density-level above 1.03'),
        ('density-level between 1.027-1.03', 'density-level between 1.027-1.03'),
        ('density-level below 1.03', 'density-level below 1.03'),
]
    quality_test_report= models.CharField(max_length=50, choices=DENSITY_CHOICES,default='1.027-1.03')
    price = models.FloatField()
    description = models.TextField()
    

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)        
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)
    

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=6,null=True)
    house_name = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=10,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field
    is_paid = models.BooleanField(default=False)
    status_choices = [
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    delivery_status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    cart = models.ManyToManyField(Cart)  # Add this field


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    is_successful = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100)  # Add this field

    def __str__(self):
        return f"Payment of {self.amount} by {self.order.user.username} on {self.payment_date}"

class SampleTestReport(models.Model):
    CATEGORY_CHOICES = [
        ('Cow', 'Cow Milk'),
        ('Goat', 'Goat Milk'),
        ('Buffalo', 'Buffalo Milk'),
    ]

    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sample_test_reports')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    density = models.DecimalField(max_digits=5, decimal_places=2)
    bacterial_content = models.DecimalField(max_digits=5, decimal_places=2)
    turbidity = models.DecimalField(max_digits=5, decimal_places=2)
    somatic_cell_count = models.PositiveIntegerField()
    lactose_content = models.DecimalField(max_digits=5, decimal_places=2)
    protein_content = models.DecimalField(max_digits=5, decimal_places=2)
    fat_content = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.seller.username} - {self.category} Milk Test Report"