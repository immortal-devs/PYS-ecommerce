from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.conf import settings
from django.db import IntegrityError
from datetime import datetime, timedelta, date
import math, random
import json
import random
from .models import Address, Admin_detail, Customer, Order, OrderItem, Product, shopping_cart
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
MERCHANT_KEY = 'j4zE3okbkZGg71&Z'

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
    total=subtotal=totaltax=0
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        context["cid"]=cid
        q=Customer.objects.get(id=cid)
        context["name"]=name
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                price=int(i.product.price)
                totalprice=i.quantity*i.product.price
                pname=i.product.name
                quantity=i.quantity
                tax=int(price*0.18)
                totaltax+=tax*quantity
                price=price-tax
                subtotal += price*quantity
                context.setdefault("products",[]).append([pname,price,quantity,totalprice,tax,i.product.id])
                address=q.address
                context["address"]=address
                custaddress=", ".join(map(str,[address.first_len,address.second_len,address.city,address.state,address.pincode]))
                context["custaddress"]=custaddress
                
    invoiceno=int(random.random() * 1000000)
    context["invoiceno"]=invoiceno
    request.session['invoiceno']=invoiceno
    total=int(subtotal) + int(totaltax)
    context["subtotal"]=subtotal
    context["totaltax"]=int(totaltax)
    context["total"] = total
    request.session['total']=total
    return render(request, 'receipt.html', context)

def checkout(request):
    context={}
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        q=Customer.objects.get(id=cid)
        context={}
        context["name"]=name 
        total=totalQuantity=0
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                price=i.product.price
                pname=i.product.name
                quantity=i.quantity
                totalprice=i.quantity*i.product.price
                totalQuantity+=quantity
                total += totalprice
                context.setdefault("products",[]).append([pname,price,quantity,totalprice,i.product.id])
        context["totalQuantity"]=totalQuantity        
        context["total"] = total
        context["customer"]=q
        context["address"]=q.address
        print(context)
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
            request.session['name'] = i.firstname.capitalize()
            request.session['email'] = i.email
            request.session['cid'] = i.id 
            return HttpResponseRedirect('/shop')
    else:
        return render(request, 'login.html', {'error': 'Email Or Password is incorrect.'})

def verificationsocial(request):
    for i in User.objects.all():
        if User.is_authenticated:
            request.session['name'] = i.first_name.capitalize()
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
    for i in Customer.objects.all():
        if email == i.email:
            return render(request, 'signup.html', {'error': 'This email is already in use!!'})
    if pass1 == pass2:
        s = Customer(firstname=firstname, lastname=lastname, email=email, password=pass1, mobile_no=mobileno)
        s.save() 
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
    if request.session.get('cid'):
        cid = request.session.get('cid')
        q=Customer.objects.get(id=cid)
        for i in shopping_cart.objects.all():
            if i.customer_id==q.id:
                carttotalq += i.quantity               
    if request.session.get('name'):
        name = request.session.get('name')
        context['name']= name
        context["carttotalq"]=carttotalq
        print("name: ",name)
        print("cid: ",cid)
        return render(request, 'shop.html', context)
    else:
        print("name: ")
        print("cid: ")
        return render(request, 'shop.html', context)

def myaccount(request):
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        q=Customer.objects.get(id=cid)
        context={}
        context["name"]=name
        context["custid"]=q.id
        context["customer"]=q
        address=q.address
        context["address"]=address
        custaddress=", ".join(map(str,[address.first_len,address.second_len,address.city,address.state,address.pincode]))
        context["custaddress"]=custaddress
        return render(request, 'myaccount.html', context)

def updatedetail(request,id):
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid = request.session.get('cid')
        q=Customer.objects.get(id=id)
        context={}
        context["name"]=name
        qwertyz = request.POST.get('firstname')
        q.firstname = request.POST.get('firstname')
        q.lastname = request.POST.get('lastname')
        q.email = request.POST.get('email')
        q.gender = request.POST.get('gender')
        q.mobile_no = request.POST.get('mobile_no')
        address=q.address
        address.first_len=request.POST.get('first_len')
        address.second_len=request.POST.get('second_len')
        address.city=request.POST.get('city')
        address.state=request.POST.get('state')
        address.pincode=request.POST.get('pincode')
        address.save()
        q.save()
        return HttpResponseRedirect('/myaccount/')

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
    for i in Customer.objects.all():
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
            target = Customer.objects.get(email=request.session['email2'])
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
        q=Customer.objects.get(id=cid)
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
        q=Customer.objects.get(id=cid)
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
    q=Customer.objects.get(id=cid)
    if shopping_cart.objects.filter(customer_id=q.id):
        shopping_cartq=shopping_cart.objects.filter(id=id)
        shopping_cartq.delete()
        return redirect('/cart')

def addquantity(request,id):
    cid = request.session.get('cid')
    q=Customer.objects.get(id=cid)
    if shopping_cart.objects.filter(customer_id=q.id):
        shopping_cartq=shopping_cart.objects.get(id=id)
        shopping_cartq.quantity=min(int(shopping_cartq.quantity)+1,10)
        shopping_cartq.save()
        return redirect('/cart')

def removequantity(request,id):
    cid = request.session.get('cid')
    q=Customer.objects.get(id=cid)
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
    q=Customer.objects.get(id=cid)
    for i in shopping_cart.objects.all():
        if i.product.id==id and i.customer_id==q.id:
            i.quantity=min(int(i.quantity)+1,10)
            i.save()
            return redirect('/shop')
    quantityq=1
    if request.session.get('name') and request.session.get('cid'):
        name = request.session.get('name')
        cid=request.session.get('cid')
        customerq=Customer.objects.get(id=cid)
        c=shopping_cart(product=productq,quantity=quantityq,customer=customerq)
        c.save()
        return redirect('/shop')
    else:
        return redirect('/shop')
    
def search (request):
    searchdict={
         "Gren":"Green", "Grn":"Green", "Greeen":"Green",
        "Llow":"Yellow","Yelow":"Yellow","Ylw":"Yellow",
        "Balek":"Black","Blk":"Black","Bleck":"Black",
        "Woman":"Women","wman":"Women","Wmn":"Women",
        "Man":"Men","Mn":"Men",
        "Kid":"Kids","ked":"Kids","Child":"Kids","Cild":"kids","Children":"Kids","chidren":"Kids","cld":"Kids","cheldren":"Kids","chaldran":"Kids",
    } 
    search=""
    context={}
    search1list=[]
    if request.session.get('name'):
        name = request.session.get('name')
        context['name']= name
    search=request.POST.get('searchq').capitalize()
    print(search)
    if search in searchdict.keys():
        search=searchdict[search]
    cnt1=0   
    for products in Product.objects.all():
        categoryp=products.category
        if search in categoryp:
            if cnt1<15:
                cnt1+=1
                search1list.append(products)
            else:
                break
    context["search"]=search
    context["search1list"]=search1list
    return render(request, 'searchitems.html', context)

@csrf_exempt
def payment(request):
    email = 'yashsuhagiya401@gmail.com'
    orderid=request.session.get("invoiceno")
    amount=request.session.get("total")
    param_dict={
        'MID': 'UkrRLw57778088991509',
        'ORDER_ID': str(orderid),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://127.0.0.1:8000/paytm/',

    }
    
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return  render(request, 'paytm.html', {'param_dict': param_dict})

def order(request,response_dict):
        print("order func")
        cid = request.session.get('cid')
        s=Order( customer=cid, status="Done", transaction_id=response_dict['TXNID'])
        s.save()
        print(" order func end")

@csrf_exempt
def paytm(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    print(verify)
    print(response_dict)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            
        else:
            print('order was not successful because' + response_dict['RESPMSG'])

    order(request, response_dict)
    print("after order func")
    return HttpResponse('done')

    