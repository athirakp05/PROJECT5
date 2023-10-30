from django.db import models
from farm.models import Seller

class p_Category(models.Model):
    category = models.CharField(max_length=50, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

class Product(models.Model):
    p_code = models.AutoField(primary_key=True, unique=True)
    p_name = models.CharField(max_length=50, null=False)
    mfg_date = models.DateField()
    expiry_date = models.DateField()
    grade_level = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    category = models.ForeignKey(p_Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', default='default.jpg')

    def __str__(self):
        return self.p_name
