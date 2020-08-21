from django.db import models
from django.contrib.auth.models import AbstractUser
from userapp.models import User
from pdapp.models import *

# Create your models here.

class Review(models.Model):
    product =  models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date  = models.DateField(null = True, auto_now=True) #리뷰 쓴 날짜
    content  = models.TextField(null = True)
    star = models.IntegerField(null = True) #별점

class Album(models.Model): #사진첩
    bodypd = models.ForeignKey(Product , null = True, on_delete = models.CASCADE, related_name='bodypd') #Product에서 두개 선택해랑
    lenspd = models.ForeignKey(Product , null = True, on_delete = models.CASCADE, related_name='lenspd')
    date = models.DateField(null = True, auto_now=True)
    pic = models.ImageField(null = True, upload_to="%Y/%m/%d")
    user = models.ForeignKey(User,on_delete=models.CASCADE)


#class Buy(models.Model): #구매

    #1. 상품 판매량, 2. 구매수량 3.  배송상태, 4.결제수단(불리안 True-무통장, False-카드)
    #가져올것들-제품사진, 제품정보, 가격, 주문자정보
class Buy(models.Model):
    countbuy= models.IntegerField(null= True) #구매수량 : 사용자가 선택
    dcheck = models.CharField(max_length=15, null = True) # 배송확인
    pay = models.BooleanField(null =True) #결제수단(True = 무통장/ False = 카드)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)#상품 외래키로 가져오기
    user = models.ForeignKey(User, on_delete = models.CASCADE) #주문자 정보 외래키로 가져오기