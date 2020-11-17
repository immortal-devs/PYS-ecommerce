from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.conf import settings

from shop.models import Product, Admin_detail, OrderItem

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
        products = Product.objects.all().order_by('-id')
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

def editproduct(request,id):
    context={}
    product = Product.objects.get(id=id)
    pname = product.name
    price = product.price
    image = product.imageURL
    category = product.category
    stock = product.stock
    color = product.color
    size = product.size
    description = product.description
    rating = product.rating
    discount = product.discount
    context.setdefault("products",[]).append([pname,price,image,category,stock,color,size,description,rating,discount,id])
    return render(request, 'editproduct.html', context)

def editproductdata(request,id):
    name = request.POST.get("name")
    price = request.POST.get("price")
    category = request.POST.get("category")
    stock = request.POST.get("stock")
    color = request.POST.get('color')
    size = request.POST.get('size')
    desc = request.POST.get('description')
    discount = request.POST.get('discount')

    q = Product.objects.get(id=id)
    q.name=name
    q.price=price
    q.category=category
    q.stock=stock
    q.color=color
    q.size=size
    q.description=desc
    q.discount=discount
    q.save()
    return HttpResponseRedirect('/admin_role/')

def orders(request):
    context={}
    if request.session.get('username'):
        username = request.session.get('username')
        context['username']= username
    for i in OrderItem.objects.all().order_by('-id'):
        price=i.product.price
        pname=i.product.name
        quantity=i.quantity
        image=i.product.imageURL
        totalprice=i.quantity*i.product.price
        orderitemid=i.id
        date=i.date_added
        status=i.delivered
        context.setdefault("products",[]).append([pname,price,quantity,totalprice,image,i.product.id,date,orderitemid,status])
    return render(request, 'orders.html', context)

def orderstatus(request,id):
    print("order status start")
    if OrderItem.objects.filter(id=id):
        q=OrderItem.objects.get(id=id)
        if q.delivered != "Delivered" and q.delivered != "Returned" and q.delivered != "Canceled":
            q.delivered="Delivered"
            q.save()
        return HttpResponseRedirect('/orders/')

       