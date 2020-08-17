from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError

# Create your views here.
from .models import Address, Admin_detail, Customer, Order, OrderItem, Product, shopping_cart, UserProfile

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
    for i in UserProfile.objects.all():
        if email == i.email and password == i.password:
            request.session['name'] = i.firstname
            request.session['email'] = i.email
            return HttpResponseRedirect('/shop/')
    else:
        return render(request, 'login.html', {'error': 'Email Or Password is incorrect.'})

def signup(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'signup.html', context)

def registrationdata(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    mobileno = request.POST.get('mobileno')
    pass1 = request.POST.get('password')
    pass2 = request.POST.get('confirmpassword')
    for i in UserProfile.objects.all():
        if email == i.email:
            return render(request, 'signup.html', {'error': 'This email is already in use!!'})
    if pass1 == pass2:
        s = UserProfile(firstname=firstname, lastname=lastname, email=email,password=pass1,mobile_no=mobileno)
        s.save()
        request.session['name'] = firstname
        request.session['email'] = email
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'signup.html', {'error': 'Re Enter same password!!'})

def category(request):
    context = {}
    return render(request, 'category.html', context)
