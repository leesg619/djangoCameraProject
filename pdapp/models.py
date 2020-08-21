from django.db import models
from django.contrib.auth.models import AbstractUser

# from userapp.models import User

# Create your models here.
class LensType(models.Model):#lenstype과 bodytype은 type으로 통일했습니다(바디 or 렌즈)로
    lname=models.CharField(max_length=200, null=True)#안써

class BodyType(models.Model):#안써
    filmb=models.CharField(max_length=200, null=True) #안써
    digitalb=models.CharField(max_length=200, null=True) #안써

class Brand(models.Model):
    bname = models.CharField(max_length=50, null=True)

class Type(models.Model):
    pdtype=models.CharField(max_length = 10 , null = True)
    
    def __str__(self):
        return self.pdtype

class Product(models.Model):
    pdname = models.CharField(max_length = 100, null = True)
    brand = models.CharField(max_length = 100, null = True)
    price = models.IntegerField(null = True)
    pic = models.ImageField(null = True, upload_to="%Y/%m/%d")
    stars = models.IntegerField(null = True) #별점
    # bodytype = models.ForeignKey(BodyType, null = True , on_delete = models.CASCADE)
    # lenstype = models.ForeignKey(LensType, null = True , on_delete = models.CASCADE)
    pdsale = models.IntegerField(null = True)#상품판매량(구매할때마다 하나씩 오르게 - 싸이월드 투데이처럼?) 
    countbuy = models.IntegerField(null=True) #구매수량 외래키로
    pdtype = models.ForeignKey(Type,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.pdname

class Star(models.Model):
    pdname = models.ForeignKey(Product, on_delete = models.CASCADE)
    pdtype = models.ForeignKey(Type,null=True, on_delete=models.CASCADE)
    star = models.IntegerField(null = True)


    class Meta:
        ordering=['-star']


    # {}에 묶어 같이 가져옴
    def __str__(self):
        return '{} {}'.format(self.pdname.pdname, self.star)
