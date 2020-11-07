from django_mysql.models import ListCharField
from django.db import models,migrations

class Address(models.Model):
	first_len = models.CharField(max_length=200,null=False)
	second_len = models.CharField(max_length=200,null=False)
	city = models.CharField(max_length=200,null=False)
	state = models.CharField(max_length=30,null=False)
	pincode = models.IntegerField( null=False)
	primary_address = models.BooleanField(default=False)

	def __str__(self): 
         return self.first_len+" "+self.second_len

class Customer(models.Model):
	firstname = models.CharField(max_length=200,null=True)
	lastname = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)
	password = models.CharField(max_length=200,null=True)
	mobile_no = models.BigIntegerField(null=True,blank=True)
	gender = models.CharField(max_length=20,default="Male")
	search = ListCharField(
		base_field = models.CharField(max_length=10),
		size = 5,
		max_length = (5*11)
	)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.id)

class Product(models.Model):
	RATE = (
        ('1', 'Very Low'),
        ('2', 'Low'),
        ('3', 'Avarage'),
		('4', 'Good'),
		('5', 'Very Good'),
    )

	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
	image = models.ImageField(null=True, blank=True)
	category = ListCharField(
		base_field = models.CharField(max_length=10),
		size = 5,
		max_length = (5*11),
	)
	stock = models.IntegerField(default=0)
	color = models.CharField(max_length=20,null=True)
	size = ListCharField(
		base_field = models.CharField(max_length=3),
		size = 6,
		max_length = (6*4),
	)
	description = models.CharField(max_length=200,null=True)
	rating = models.IntegerField(choices=RATE,default=5)
	discount = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	STATUS = (
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered'),
	)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=40, null=True, choices=STATUS)
	transaction_id = models.CharField(max_length=200,null=True,blank=True,default="00000000")
	def __str__(self):
		return self.transaction_id

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( default=1)
	date_added = models.DateTimeField(auto_now_add=True)
	delivered = models.CharField(max_length=50,default="Ordered")

	def __str__(self):
		return str(self.product.name+" "+self.order.customer.firstname)
	

class shopping_cart(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( null=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)

class paymentdata(models.Model):
	orderid = models.CharField(max_length=200)
	cid = models.CharField(max_length=50)
	