from django.db import models
from django.contrib.auth.models import User
from dj.choices import Choice, Choices
from dj.choices.fields import ChoiceField
# Create your models here.


class Address(models.Model):
	# address_id = models.AutoField()
	first_len = models.CharField(max_length=200,null=False)
	second_len = models.CharField(max_length=200,null=False)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=30)
	pincode = models.IntegerField(max_length=6)
	primary_address = models.BooleanField(default=False)

class Customer(models.Model):
	# customer_id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	email = models.CharField(max_length=200,null=False)
	password = models.CharField(max_length=15,null=False)
	gender = models.CharField(max_length=20)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	birthdate = models.DateField()
	mobile_no = models.IntegerField(max_length=10)
	search = models.CharField(max_length=1000,null=True)

class Product(models.Model):
	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200,null=True)
	price = models.DecimalField()
	image = models.ImageField(null=True, blank=True)
	category = models.CharField(max_length=30)
	stock = models.IntegerField()

class Order(models.Model):
	# order_id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=False, blank=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	transaction_id=models.CharField(max_length=200,null=True)

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=False, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=False, blank=True)
	quantity = models.IntegerField()
	date_added = models.DateTimeField(auto_now_add=True)

class shopping_cart(models.Model):
	product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=False, blank=True)
	quantity = models.IntegerField()
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)



class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)
