from django.shortcuts import render
from .models import Customer,Product,OrderItem,Order
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf

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
    context.update(csrf(request))
    return render(request, 'login.html', context)

def verification(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    for i in Customer.objects.all():
        if email == i.email and password == i.password:
            request.session['name'] = i.firstname
            request.session['email'] = i.email
            return HttpResponseRedirect('/shop/')
    else:
        return render(request, 'login.html', {'error': 'Enter a correct information'})

def signup(request):
    context = {}
    return render(request, 'signup.html', context)

def category(request):
    context = {}
    return render(request, 'category.html', context)
