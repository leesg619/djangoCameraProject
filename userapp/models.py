from django.db import models
from django.contrib.auth.models import AbstractUser
from pdapp.models import Product
# Create your models here.

class User(AbstractUser):
    #username = models.TextField(null = True)
    #password
    address = models.CharField(max_length = 100,null = True)
    phone = models.TextField(null = True)
    age = models.TextField(null = True)
    gender = models.BooleanField(null=True) #남자True 여자 False

class MyProduct(models.Model):
    mypd = models.ForeignKey(Product, on_delete = models.CASCADE)
    User = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(null = True, auto_now=True) #구매날짜

