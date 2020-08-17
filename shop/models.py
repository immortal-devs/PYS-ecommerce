from django.db import models,migrations

class UserProfile(models.Model):
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	email = models.CharField(max_length=200,null=False)
	password = models.CharField(max_length=15,null=False)
	mobile_no = models.BigIntegerField()


class Address(models.Model):
	# address_id = models.AutoField()
	first_len = models.CharField(max_length=30,null=True)
	second_len = models.CharField(max_length=30,null=True)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=30)
	pincode = models.IntegerField( null=True)
	primary_address = models.BooleanField(default=False)

class Customer(models.Model):
	# customer_id = models.AutoField(primary_key=True)
	gender = models.CharField(max_length=20)
	birthdate = models.DateField()
	search = models.CharField(max_length=1000,null=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, blank=True)

class Product(models.Model):
	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200,null=True)
	price = models.DecimalField(max_digits=5,decimal_places=2)
	image = models.ImageField(null=True, blank=True)
	category = models.CharField(max_length=30)
	stock = models.IntegerField( null=True)

class Order(models.Model):
	# order_id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
	complete = models.BooleanField(default=True,null=True,blank=True)
	transaction_id=models.CharField(max_length=200,null=True)

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.IntegerField( null=True)
	date_added = models.DateTimeField(auto_now_add=True)

class shopping_cart(models.Model):
	product= models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.IntegerField( null=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)
