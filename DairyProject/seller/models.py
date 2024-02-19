from django.db import models
from farm.models import CustomUser

class DeliveryBoy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True)
    driving_license = models.FileField(upload_to='driving_licenses/', null=True, unique=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Field to track account status

    def __str__(self):
        return self.name

    
class DeliveryBoyEdit(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    delivery_boy = models.OneToOneField(DeliveryBoy, on_delete=models.CASCADE)
    driving_license = models.FileField(upload_to='driving_licenses/', null=True, unique=True)
    house_name = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    pin_code = models.IntegerField(null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, null=True)
    age = models.IntegerField(null=True, blank=True, default=None)
    email = models.EmailField(unique=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='vet_profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Delivery(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
    ]
    customer = models.ForeignKey('farm.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.product} - {self.status}"

class ApprovalRequest(models.Model):
    delivery_boy = models.OneToOneField(DeliveryBoy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Approval Request for {self.delivery_boy.name}"