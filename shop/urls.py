from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.shop, name="shop"),
	path('login/', views.login, name="login"),
	path('login/verification', views.verification, name="verification"),
	path('signup/', views.signup, name="signup"),
	path('category/', views.category, name="category"),
	path('product/', views.product, name="product"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	
]