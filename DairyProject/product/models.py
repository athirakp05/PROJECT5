from django.db import models
from farm.models import Seller


class Product(models.Model):
    p_code = models.AutoField(primary_key=True, unique=True)
    p_name = models.CharField(max_length=50, null=False)
    mfg_date = models.DateField()
    expiry_date = models.DateField()
    GRADE_CHOICES = [
        ('1', 'A'),
        ('2', 'B'),
        ('3', 'C'),
]
    grade_level = models.CharField(max_length=10, choices=GRADE_CHOICES,default='A')
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    description = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    
    CATEGORY_CHOICES = [
    ('Milk', 'Milk'),
    ('Curd', 'Curd'),
    ('Paneer', 'Paneer'),
    ('Ghee', 'Ghee'),
    ('Butter', 'Butter'),
    ('Cheese', 'Cheese'),
]
    categories = models.CharField(max_length=10, choices=CATEGORY_CHOICES,default='milk')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

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
    cattle = models.CharField(max_length=10, choices=CATTLE_CHOICES, default='Cow')
    collection_date = models.DateField()
    COLLECTION_CHOICES = [
        ('1', 'ForeNoon'),
        ('2', 'AfterNoon'),
]
    collection_time = models.CharField(max_length=50,  choices=COLLECTION_CHOICES,default='1.027-1.03')
    quantity = models.PositiveIntegerField()
    DENSITY_CHOICES = [
        ('1', '1.03+'),
        ('2', '1.027-1.03'),
        ('3', '1.03-'),
]
    density_level = models.CharField(max_length=10, choices=DENSITY_CHOICES,default='1.027-1.03')
    price = models.FloatField()
    description = models.TextField()
