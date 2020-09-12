from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError
from datetime import datetime, timedelta, date
import math, random
from .models import Address, Admin_detail, Customer, Order, OrderItem, Product, shopping_cart, UserProfile


def product(request,id):
    context={}
    if request.session.get('name'):
        name = request.session.get('name')
        context['name']= name
    product = Product.objects.get(id=id)
    context['product']=product
    cnt1=cnt2=cnt3=0
    rproductlist1=set()
    rproductlist2=set()
    rproductlist3=set()
    relativecategory=product.category[0]
    for rproducts in Product.objects.all():
        categoryp=rproducts.category
        if relativecategory in categoryp:
            if cnt1<3 and rproducts != product:
                cnt1+=1
                rproductlist1.add(rproducts)
            elif cnt2<3 and rproducts != product:
                cnt2+=1
                rproductlist2.add(rproducts)
            elif cnt3<3 and rproducts != product:
                cnt3+=1
                rproductlist3.add(rproducts)
    context["rproducts1"]=rproductlist1
    context["rproducts2"]=rproductlist2
    context["rproducts3"]=rproductlist3
    return render(request, 'product.html', context)

def receipt(request):
    context={}
    total=subtotal=0
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        context["cid"]=cid
        q=Customer.objects.get(user_id=cid)
        context["name"]=name
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                price=i.product.price
                pname=i.product.name
                quantity=i.quantity
                totalprice=i.quantity*i.product.price
                subtotal += totalprice
                context.setdefault("products",[]).append([pname,price,quantity,totalprice,i.product.id])
    tax=float(subtotal) * 0.18
    total=float(subtotal) + tax
    context["subtotal"]=subtotal
    context["tax"]=tax
    context["total"] = total
    return render(request, 'receipt.html', context)
    

def checkout(request):
    context={}
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        q=Customer.objects.get(user_id=cid)
        context={}
        context["name"]=name
        total=0
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                price=i.product.price
                pname=i.product.name
                quantity=i.quantity
                image=i.product.imageURL
                totalprice=i.quantity*i.product.price
                total += totalprice
                cartid=i.id
                color=i.product.color
                context.setdefault("products",[]).append([pname,price,quantity,totalprice,image,cartid,color,i.product.id])
        context["total"] = total
    return render(request, 'checkout.html', context)


    # if request.user.is_authenticated:
    #     customer = request.user.customer

        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    # else:
    #     items = []
    #     order = {'get_cart_total':0,'get_cart_items':0}
    # context = {'items':items, 'order':order}
    # return render(request, 'checkout.html', context)

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
            request.session['cid'] = i.id 
            return HttpResponseRedirect('/shop')
    else:
        return render(request, 'login.html', {'error': 'Email Or Password is incorrect.'})

def verificationsocial(request):
    for i in User.objects.all():
        if User.is_authenticated:
            request.session['name'] = i.first_name
            return HttpResponseRedirect('/shop')

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
        s = UserProfile(firstname=firstname, lastname=lastname, email=email, password=pass1, mobile_no=mobileno)
        s.save()
        request.session['name'] = firstname
        c=Customer(gender="male",birthdate=date.today(),search="",address_id="1",user_id=s.id)
        c.save()
        request.session['cid'] = s.id 
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'signup.html', {'error': 'Re Enter same password!!'})

def shop(request):
    context={}
    cntm=cntw=cntk=cntn=cntb=cnts=0
    menProductList=[]
    womenProductList=[]
    kidsProductList=[]
    newProductList=[]
    bestSellerProductList=[]
    saleProductList=[]
    for products in Product.objects.all():
        categoryp=products.category
        if "Men" in categoryp:
            if cntm<3:
                cntm+=1
                menProductList.append(products)
             
        if "Women" in categoryp:
            if cntw<3:
                cntw+=1
                womenProductList.append(products)
              
        if "Kids" in categoryp:
            if cntk<3:
                cntk+=1
                kidsProductList.append(products)
               
        if "New" in categoryp:
            if cntn<3:
                cntn+=1
                newProductList.append(products)
                continue
        if "Bestseller" in categoryp:
            if cntb<3:
                cntb+=1
                bestSellerProductList.append(products) 
                continue   
        if "Sale" in categoryp:
            if cnts<3:
                cnts+=1
                saleProductList.append(products)   
                continue 
    context["men"]=menProductList
    context["women"]=womenProductList
    context["kids"]=kidsProductList
    context["sale"]=saleProductList
    context["new"]=newProductList
    context["bestseller"]=bestSellerProductList
    carttotalq=0
    if  request.session.get('cid'):
        cid = request.session.get('cid')
        q=Customer.objects.get(user_id=cid)
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                carttotalq += i.quantity               
    if request.session.get('name'):
        name = request.session.get('name')
        context['name']= name
        context["carttotalq"]=carttotalq
        return render(request, 'shop.html', context)
    else:
        return render(request, 'shop.html', context)

def logout(request):
    del request.session['name']
    del request.session['cid']
    return HttpResponseRedirect('/shop/')

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
    title = 'Category'
    if request.session.get('name'):
        name = request.session.get('name')
        context = {'name': name, 'title': title}
        return render(request, 'category.html', context)
    else:
        context = {'title': title}
        return render(request, 'category.html', context)

def totalQuantity(request):
    total=0
    if  request.session.get('cid'):
        cid = request.session.get('cid')
        q=Customer.objects.get(user_id=cid)
        context={}
        total=0
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                total += i.quantity
               
        context["total"] = total
        return render(request, 'cart.html', context)

def cart(request):
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        q=Customer.objects.get(user_id=cid)
        context={}
        context["name"]=name
        total=0
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                price=i.product.price
                pname=i.product.name
                quantity=i.quantity
                image=i.product.imageURL
                totalprice=i.quantity*i.product.price
                total += totalprice
                cartid=i.id
                color=i.product.color
                context.setdefault("products",[]).append([pname,price,quantity,totalprice,image,cartid,color,i.product.id])
        context["total"] = total
        return render(request, 'cart.html', context)
    else:
        context = {} 
        return render(request, 'cart.html', context)

def deleteFromCart(request,id):
    cid = request.session.get('cid')
    q=Customer.objects.get(user_id=cid)
    if shopping_cart.objects.filter(customer_id=q.id):
        shopping_cartq=shopping_cart.objects.filter(id=id)
        shopping_cartq.delete()
        return redirect('/cart')

def addquantity(request,id):
    cid = request.session.get('cid')
    q=Customer.objects.get(user_id=cid)
    if shopping_cart.objects.filter(customer_id=q.id):
        shopping_cartq=shopping_cart.objects.get(id=id)
        shopping_cartq.quantity=min(int(shopping_cartq.quantity)+1,10)
        shopping_cartq.save()
        return redirect('/cart')

def removequantity(request,id):
    cid = request.session.get('cid')
    q=Customer.objects.get(user_id=cid)
    if shopping_cart.objects.filter(customer_id=q.id):
        shopping_cartq=shopping_cart.objects.get(id=id)
        shopping_cartq.quantity-=1
        if shopping_cartq.quantity <= 0:
            return redirect('/cart/delete/'+str(id))
        shopping_cartq.save()
        return redirect('/cart')
    
def contact(request):
    context = {} 
    if request.session.get('name'):
        name = request.session.get('name')
        context["name"]=name
    return render(request, 'contact.html', context)

def addtocart(request,id):
    productq= Product.objects.get(id=id)
    cid = request.session.get('cid')
    q=Customer.objects.get(user_id=cid)
    for i in shopping_cart.objects.all():
        if i.product.id==id and i.customer_id==q.id:
            i.quantity=min(int(i.quantity)+1,10)
            i.save()
            return redirect('/shop')
    quantityq=1
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid=request.session.get('cid')
        customerq=Customer.objects.get(user_id=cid)
        c=shopping_cart(product=productq,quantity=quantityq,customer=customerq)
        c.save()
        return redirect('/shop')
    else:
        return redirect('/shop')

def search (request):
    search=""
    context={}
    if request.session.get('name'):
        name = request.session.get('name')
        context['name']= name
    search=request.POST.get('searchq').capitalize()
    cnt1=0
    search1list=[]
    for products in Product.objects.all():
        categoryp=products.category
        if search in categoryp:
            if cnt1<15:
                cnt1+=1
                search1list.append(products)
            else:
                break
    context["search1list"]=search1list
    return render(request, 'searchitems.html', context)