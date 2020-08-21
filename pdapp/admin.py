from django.contrib import admin
from .models import Product, BodyType, LensType, Brand, Star,Type

# Register your models here.
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(BodyType)
admin.site.register(LensType)
admin.site.register(Star)
admin.site.register(Type)