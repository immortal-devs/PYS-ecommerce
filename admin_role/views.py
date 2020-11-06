from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.conf import settings

from shop.models import Product, Admin_detail, OrderItem

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
    color = request.POST.get('color')
    size = request.POST.get('size')
    desc = request.POST.get('description')
    discount = request.POST.get('discount')

    s = Product(name=name,category=category,price=price,stock=stock,size=size,image=image,color=color,description=desc,discount=discount)
    s.save()
    return HttpResponseRedirect('/admin_role/')

def orders(request):
    context={}
    if request.session.get('username'):
        username = request.session.get('username')
        context['username']= username
    for i in OrderItem.objects.all():
        price=i.product.price
        pname=i.product.name
        quantity=i.quantity
        image=i.product.imageURL
        totalprice=i.quantity*i.product.price
        cartid=i.id
        # color=i.product.color
        date=i.date_added
        context.setdefault("products",[]).append([pname,price,quantity,totalprice,image,cartid,date,i.product.id])
        print(pname,totalprice,i.product.id)
    print("qwqw")
    print(context)
    return render(request, 'orders.html', context)