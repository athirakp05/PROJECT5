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
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    pH = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    taste = models.CharField(max_length=50, null=True)
    odor = models.CharField(max_length=50, null=True)
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    turbidity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    color = models.CharField(max_length=50, null=True)
    grade = models.CharField(max_length=50, null=True)

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


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    is_successful = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100)  # Add this field

    def __str__(self):
        return f"Payment of {self.amount} by {self.order.user.username} on {self.payment_date}"


