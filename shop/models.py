from django.db import models,migrations

class UserProfile(models.Model):
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	email = models.CharField(max_length=200,null=False)
	password = models.CharField(max_length=15,null=False)
	mobile_no = models.BigIntegerField(null=True,blank=True)

	def __str__(self):
		return self.firstname

class Address(models.Model):
	# address_id = models.AutoField()
	first_len = models.CharField(max_length=30,null=False)
	second_len = models.CharField(max_length=30,null=False)
	city = models.CharField(max_length=200,null=False)
	state = models.CharField(max_length=30,null=False)
	pincode = models.IntegerField( null=False)
	primary_address = models.BooleanField(default=False)

	def __str__(self): 
         return self.first_len+" "+self.second_len

class Customer(models.Model):
	# customer_id = models.AutoField(primary_key=True)
	gender = models.CharField(max_length=20,default="male")
	birthdate = models.DateField()
	search = models.CharField(max_length=1000,null=True,blank=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, blank=True)

	def __str__(self):
	 return self.user.firstname

class Product(models.Model):
	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5,decimal_places=2,default=0)
	image = models.ImageField(null=True, blank=True)
	category = models.CharField(max_length=30)
	stock = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Order(models.Model):
	# order_id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=True)
	complete = models.BooleanField(default=False)
	transaction_id=models.CharField(max_length=200,null=True,blank=True,default="00000000")

	def __str__(self):
		return self.transaction_id

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( default=1)
	date_added = models.DateTimeField(auto_now_add=True)

	
	def __str__(self):
		return str(self.product.name+" "+self.order.customer.name)
	

class shopping_cart(models.Model):
	product= models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( null=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)
