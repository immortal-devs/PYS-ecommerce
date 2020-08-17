from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError
import math, random

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
            return HttpResponseRedirect('/shop')
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
    if len(mobileno) != 10:
        return render(request, 'signup.html', {'error': 'Enter correct mobile number!!'})
    if type(mobileno) == str:
        return render(request, 'signup.html', {'error': 'Enter correct mobile number!!'})
    if pass1 == pass2:
        s = UserProfile(firstname=firstname, lastname=lastname, email=email, password=pass1, mobile_no=mobileno)
        s.save()
        request.session['name'] = firstname
        request.session['email'] = email
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'signup.html', {'error': 'Re Enter same password!!'})

def forgotpassword(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'forgotpassword.html', context)

def newpassword(request):
    c = {}
    c = c.update(csrf(request))
    email = request.POST.get('email')
    request.session['email2'] = email
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    for i in UserProfile.objects.all():
        if i.email == email:
            subject = 'Your confidential OTP'
            message = 'Your OTP is ' + OTP
            from_email = settings.EMAIL_HOST_USER
            to_list = [i.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            request.session['otp'] = OTP
            return render(request, 'newpassword.html', c)
    else:
        return render(request, 'forgotpassword.html', {'error': 'Enter registered email'})

def addnewpassword(request):
    if request.session.get('otp') is None:
        password = request.POST.get('password', '')
        cpass = request.POST.get('confirmpassword', '')
        if password != cpass:
            return render(request, 'newpassword.html', {'error': 'Can not change password. Your both Passwords are different'})
        else:
            target = UserProfile.objects.get(email=request.session['email2'])
            target.password = password
            target.save()
            del request.session['email2']
            return render(request, 'login.html', {'msg': 'Password successfully changed.'})
    else:
        otp = request.POST.get('otp')
        if otp == request.session['otp']:
            del request.session['otp']
            return render(request, 'newpassword.html')
        else:
            return render(request, 'newpassword.html', {'error': 'Enter correct OTP'})

def category(request):
    context = {}
    return render(request, 'category.html', context)
