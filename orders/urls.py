from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("registered", views.registered, name="registered"),
    path("login", views.login_page, name="login_page"),
    path("loggingIn", views.login_view, name="login_view"),
    path("loggingOut", views.logout_view, name="logout_view"),
    path("addtocart", views.addtocart, name="addtocart"),
    path("cart", views.cart, name="cart"),
    path("payment", views.payment, name="payment"),
    path("<int:productid>", views.select, name="select")
]
