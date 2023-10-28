from django.contrib.auth.models import Group
from django.db import models

class CustomGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name