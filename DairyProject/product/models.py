# In product/models.py

from django.db import models

class Product(models.Model):
    productCode = models.AutoField(primary_key=True)
    productType = models.CharField(max_length=50)

    def __str__(self):
        return self.productType

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productName = models.CharField(max_length=50)
    mfgDate = models.DateField()
    expiryDate = models.DateField()
    gradeLevel = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.productName

# Define other models following a similar pattern
