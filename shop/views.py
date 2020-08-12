from django.shortcuts import render
from .models import *
# Create your views here.
def shop(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'shop.html', context)

def product(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'product.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'checkout.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)

def signup(request):
    context = {}
    return render(request, 'signup.html', context)

def category(request):
    context = {}
    return render(request, 'category.html', context)
