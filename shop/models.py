from django.db import models

class Address(models.Model):
	address_id = models.AutoField()
	first_len = models.CharField(max_length=200,null=False)
	second_len = models.CharField(max_length=200,null=True)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=30)
	pincode = models.IntegerField(max_length=6)
	primary_address = models.BooleanField(default=False)
	customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

class Customer(models.Model):
	customer_id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	email = models.CharField(max_length=200,null=False)
	password = models.CharField(max_length=15,null=False)
	gender = models.CharField(max_length=10)
	address_id = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	birthdate = models.DateField()
	mobile_no = models.IntegerField(max_length=10)

class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200,null=True)
	price = models.DecimalField(max_digits=5,decimal_places=2)
	image = models.ImageField(null=True, blank=True)
	category = models.CharField(max_length=30)
	stock = models.IntegerField()

class Order(models.Model):
	order_id = models.AutoField(primary_key=True)
	customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=False, blank=True)
	address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=False, blank=True)

class OrderItem(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=False, blank=True)
	order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=False, blank=True)
	quantity = models.IntegerField()
	date_ordered = models.DateTimeField(auto_now_add=True)

class Customer_search(models.Model):
	customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	search = models.CharField()

class Shopping_cart(models.Model):
	shopping_id = models.AutoField(primary_key=True)
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=False, blank=True)
	quantity = models.IntegerField()
	customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)
