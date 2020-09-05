from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError
import math, random

from shop.models import Product

# Create your views here.

def admin(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)

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