from django.db import models
from django.contrib.auth.models import User
from dj.choices import Choice, Choices
from dj.choices.fields import ChoiceField
# Create your models here.

class Address(models.Model):
	# address_id = models.AutoField()
	first_len = models.CharField(max_length=30, null=False)
	second_len = models.CharField(max_length=30, null=False)
	city = models.CharField(max_length=20)
	state = models.CharField(max_length=20)
	pincode = models.IntegerField()
	primary_address = models.BooleanField(default=False)

class Customer(models.Model):
	# customer_id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=20,null=False)
	lastname = models.CharField(max_length=20,null=False)
	email = models.CharField(max_length=30,null=False)
	password = models.CharField(max_length=15,null=False)
	gender = models.CharField(max_length=5)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	birthdate = models.DateField()
	mobile_no = models.BigIntegerField()
	search = models.CharField(max_length=100,null=True)

class Product(models.Model):
	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20,null=True)
	price = models.DecimalField(max_digits=5,decimal_places=2)
	image = models.ImageField(null=True, blank=True)
	category = models.CharField(max_length=30)
	stock = models.IntegerField()

class Order(models.Model):
	# order_id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	transaction_id = models.CharField(max_length=20,null=True)

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField()
	date_added = models.DateTimeField(auto_now_add=True)

class shopping_cart(models.Model):
	product= models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField()
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=15)
