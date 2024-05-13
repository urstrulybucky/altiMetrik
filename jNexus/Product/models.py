from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    manufacture_date = models.DateField()
    warranty_information = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=50)


    