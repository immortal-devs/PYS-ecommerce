from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	 
	path('', views.shop, name="shop"),
	path('shop/', views.shop, name="shop"),
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path('verification/', views.verification, name="verification"),
	path('signup/', views.signup, name="signup"),
	path('registrationdata/', views.registrationdata, name="registrationdata"),
	path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
	path('newpassword/', views.newpassword, name="newpassword"),
	path('addnewpassword/', views.addnewpassword, name="addnewpassword"),
	path('myaccount/', views.myaccount, name="myaccount"),
	path('category/', views.category, name="category"),
	path('cart/', views.cart, name="cart"),
	path('contact/', views.contact, name="contact"),
	path('search/', views.search, name="search"),
	path('checkout/', views.checkout, name="checkout"),
	path('receipt/', views.receipt, name="receipt"),
	path('product/<int:id>', views.product, name="product"),
	path('cart/delete/<int:id>',views.deleteFromCart),
	path('cart/addquantity/<int:id>',views.addquantity),
	path('addtocart/<int:id>', views.addtocart, name="addtocart"),
	path('cart/removequantity/<int:id>',views.removequantity),
	path('updatedetail/<int:id>',views.updatedetail),
	path('payment/', views.payment, name="payment"),
	path('paytm/', views.paytm, name="paytm"),
	path('successful/', views.successful, name="successful"),
	path('unsuccessful/', views.unsuccessful, name="failed"),
	path('myorder/', views.myorder, name="myorder"),
	path('rating/<int:id>', views.rating, name="rating"),
	path('ratingdata/<int:id>', views.ratingdata, name="ratingdata"),
	path('returnproduct/<int:id>', views.returnproduct, name="return"),
	path('codpayment/', views.codpayment, name="cod"),
	path('filter/<int:filter>', views.filter, name="filter"),
]