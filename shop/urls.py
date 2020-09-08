from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	
	path('cart/addquantity/<int:id>',views.addquantity),
	path('cart/removequantity/<int:id>',views.removequantity),
    #Leave as empty string for base url
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path('verification/', views.verification, name="verification"),
	path('verification1/', views.verificationsocial, name="verification1"),
	path('signup/', views.signup, name="signup"),
	path('registrationdata/', views.registrationdata, name="registrationdata"),
	path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
	path('newpassword/', views.newpassword, name="newpassword"),
	path('addnewpassword/', views.addnewpassword, name="addnewpassword"),
	path('category/', views.category, name="category"),
	path('product/', views.product, name="product"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('', views.shop, name="shop"),
	path('shop/', views.shop, name="shop"),
	path('cart/delete/<int:id>',views.deleteFromCart),
]