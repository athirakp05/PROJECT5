from django.db import models
from farm.models import DeliveryBoy, Seller,CustomUser
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

from django.db import models
from django.utils import timezone

class MilkSample(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='milk_samples')
    collection_date = models.DateField(default=timezone.now)
    COLLECTION_CHOICES = [
        ('ForeNoon', 'ForeNoon'),
        ('AfterNoon', 'AfterNoon'),
    ]
    collection_time = models.CharField(max_length=50, choices=COLLECTION_CHOICES, default='ForeNoon')
    CATTLE_CHOICES = [
        ('Cow', 'Cow'),
        ('Buffalo', 'Buffalo'),
        ('Goat', 'Goat'),
    ]
    milk_type = models.CharField(max_length=10, choices=CATTLE_CHOICES, default='Cow')
    quantity = models.PositiveIntegerField(help_text="Enter the quantity of milk in liters")
    description = models.TextField(help_text="Enter the description")
    pH = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text="<span style='color: green;'>This Column defines PH values of the milk which ranges from 3 to 9.5 max : 6.25 to 6.90</span>")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text="<span style='color: green;'>This Column defines Temperature of the milk which ranges from 34'C to 90'C max : 34'C to 45.20'C</span>")
    taste = models.CharField(max_length=50, null=True, help_text="<span style='color: green;'>This Column defines Taste of the milk which is categorical data 0 (Bad) or 1 (Good) max : 1 (Good)</span>")
    odor = models.CharField(max_length=50, null=True, help_text="<span style='color: green;'>This Column defines Odor of the milk which is categorical data 0 (Bad) or 1 (Good) max : 0 (Bad)</span>")
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text="<span style='color: green;'>This Column defines Fat of the milk which is categorical data 0 (Low) or 1 (High) max : 1 (High)</span>")
    turbidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text="<span style='color: green;'>This Column defines Turbidity of the milk which is categorical data 0 (Low) or 1 (High) max : 1 (High)</span>")
    color = models.CharField(max_length=50, null=True, help_text="<span style='color: green;'>This Column defines Color of the milk which ranges from 240 to 255 max : 255</span>")
    grade = models.CharField(max_length=50, null=True, blank=True, help_text="<span style='color: green;'>This Column defines Grade (Target) of the milk which is categorical data Low (Bad) or Medium (Moderate) High</span>")

    def __str__(self):
        return f"Milk Sample for {self.seller.user.email} collected on {self.collection_date}"

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
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    is_successful = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100)  # Add this field

    def __str__(self):
        return f"Payment of {self.amount} by {self.order.user.username} on {self.payment_date}"


