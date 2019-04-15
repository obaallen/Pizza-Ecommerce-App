from django.contrib import admin
from .models import Product, Productline, Size, Price, Topping, AddOn, Purchase

# Register your models here.

admin.site.register(Product)
admin.site.register(Productline)
admin.site.register(Size)
admin.site.register(Price)
admin.site.register(Topping)
admin.site.register(AddOn)
admin.site.register(Purchase)
