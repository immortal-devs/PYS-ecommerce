from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.shop, name="shop"),
	path('tshirts/', views.tshirts, name="tshirts"),
	path('login/', views.login, name="login"),
	path('signup/', views.signup, name="signup"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	
]