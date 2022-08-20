from unicodedata import category
from django.db import models

# Create your models here.

class Expense(models.Model):
    name=models.CharField(default='',max_length=128)
    amount=models.IntegerField(default=0)
    category=models.CharField(default='',max_length=128)
    date=models.DateField()

    def __str__(self):
        return self.name