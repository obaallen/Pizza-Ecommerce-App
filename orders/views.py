from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Product, Productline, Topping, AddOn, Price, Size, Purchase
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {
        "products": Product.objects.all()
    }
    return render(request, "orders/index.html", context)

def register(request):
    return render(request, "registration/register.html")

def registered(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    if not username or not password:
        raise Http404("Something went wrong. Please go back and fill out your username and password")

    #register the user
    user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password,
                                     first_name=first_name,
                                     last_name=last_name)
    login(request, user)
    return redirect('index')

def login_page(request):
    return render(request, "registration/login.html")

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        raise Http404("user does not exist")
        return redirect('login_page')

def logout_view(request):
    logout(request)
    return redirect('login_page')

def select(request, productid):
    if not request.user.is_authenticated:
        return redirect('login_page')

    try:
        product = Product.objects.get(pk=productid)
        productlines = Productline.objects.all().filter(product=productid)
    except Productline.DoesNotExist:
        raise Http404("product does not exist")

    context = {
        "product": product,
        "productlines": productlines.all(),
        "toppings": Topping.objects.all(),
        "addons": AddOn.objects.all(),
        "sizes": Size.objects.all()
    }
    return render(request, "orders/selection.html", context)

def addtocart(request):
    productline = request.POST["productline"]
    productinstance = Productline.objects.get(pk=productline)
    size = request.POST["size"]
    sizeInstance = Size.objects.get(pk=size)
    addon = request.POST.get("addon", False)
    toppings = request.POST.get('toppings', False)
    price = Price.objects.get(productlines=productline, size=size)
    current_user = request.user

    purchase = Purchase()
    purchase.product = productinstance.product
    purchase.productlines = productinstance
    purchase.size = sizeInstance
    purchase.unitprice = price
    purchase.TotalPrice = price.price
    purchase.user = current_user
    purchase.status = 'New'
    purchase.save()
    context = {
        "purchases": Purchase.objects.all().filter(user=current_user),
    }
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    currentuser = request.user
    purchases = Purchase.objects.all().filter(user=currentuser, status='New')
    TotalPrice = sum(purchase.TotalPrice for purchase in purchases)
    context = {
        "purchases": purchases,
        "total_price": TotalPrice
    }
    return render(request, "orders/cart.html", context)

def payment(request):
    currentuser = request.user
    Purchase.objects.all().filter(user=currentuser).update(status='Complete')
    return render(request, "orders/payment_success.html")
