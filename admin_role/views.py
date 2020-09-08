from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError
import math, random

from shop.models import Product, Admin_detail

# Create your views here.

def adminlogin(request):
    context = {}
    return render(request, 'adminlogin.html', context)

def checkuser(request):
    username = request.POST.get("username")
    password = request.POST.get("pass")

    for i in Admin_detail.objects.all():
        if username == i.username and password == i.password:
            request.session['username'] = username
            return HttpResponseRedirect('/admin_role/')
        else:
            return render(request, 'adminlogin.html')

def admin(request):
    if request.session.get('username'):
        username = request.session.get('username')
        products = Product.objects.all() 
        context = {'products': products,'username': username}
        return render(request, 'home.html', context)
    else:
        context = {}
        return render(request, 'home.html', context)

def adminlogout(request):
    del request.session['username']
    return HttpResponseRedirect('/admin_role/')


def addproduct(request):
    context = {}
    return render(request, 'addproduct.html', context)

def checkproductdata(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    category = request.POST.get("category")
    stock = request.POST.get("stock")
    image = request.FILES['image']

    s = Product(name=name,category=category,price=price,stock=stock,image=image)
    s.save()
    return HttpResponseRedirect('/admin_role/')