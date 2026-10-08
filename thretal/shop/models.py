from tkinter.constants import CASCADE

from django.db import models
from random import randint
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='categories')


    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='subcategories')



    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=80)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=30, blank=True)
    material=models.CharField(max_length=20)
    is_best_seller=models.BooleanField(default=False)
    image=models.ImageField(upload_to='products',blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='products',blank=True, null=True)



    def __str__(self):
        return f"Image for {self.product.name}"


class CustomUser(AbstractUser):
    phone=models.IntegerField(default=0)

    is_verified=models.BooleanField(default=False)   #After verification it will set to True
    otp=models.CharField(max_length=10, null=True, blank=True)  #To store the generated otp in backend table



    def generate_otp(self):
          #for creating random otp number for verification

        otp_number=str(randint(1000,9999))+str(self.id)

        self.otp=otp_number

        self.save()



