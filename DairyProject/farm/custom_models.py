from django.contrib.auth.models import Group
from django.db import models

class CustomGroup(models.Model):
    # Add any additional fields or customizations you need for your custom group
    # For example, you can add a description field or any other relevant fields.
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)  # Add custom fields as needed

    def __str__(self):
        return self.name  # Customize the string representation as needed
