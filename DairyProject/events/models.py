# models.py
from django.db import models

class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
