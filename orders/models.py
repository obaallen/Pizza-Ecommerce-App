from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class AddOn(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} +${self.price}"

class Productline(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=64)
    require_toppings = models.IntegerField()
    require_addons = models.IntegerField()
    toppings = models.ManyToManyField(Topping, blank=True, related_name="pizza_toppings")
    addOns = models.ManyToManyField(AddOn, blank=True, related_name="subs_addOn")

    def __str__(self):
        return f"{self.name} {self.product}"

class Size(models.Model):
    size = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.size}"

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="priced_product")
    productlines = models.ForeignKey(Productline, on_delete=models.CASCADE, related_name="product_line")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="sizes")
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.productlines} {self.product} - {self.price}"

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    productlines = models.ForeignKey(Productline, on_delete=models.CASCADE, related_name="order_product_lines")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings")
    addOns = models.ManyToManyField(AddOn, blank=True, related_name="addOn")
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    unitprice = models.ForeignKey(Price, on_delete=models.CASCADE, related_name="prices")
    TotalPrice = models.FloatField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.productlines} - {self.user} - {self.status}"
