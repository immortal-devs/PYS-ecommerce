from django.urls import path

from . import views

urlpatterns = [
    #Leave as empty string for base url
	path('login/', views.login, name="login"),
	path('verification/', views.verification, name="verification"),
	path('signup/', views.signup, name="signup"),
	path('registrationdata/', views.registrationdata, name="registrationdata"),
	path('category/', views.category, name="category"),
	path('product/', views.product, name="product"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('shop/', views.shop, name="shop"),
]