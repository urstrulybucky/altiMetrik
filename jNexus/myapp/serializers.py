from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'manufacturer', 'serial_number', 'manufacture_date', 'warranty_information', 'category']