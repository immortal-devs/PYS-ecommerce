from django.contrib import admin
# Register your models here.
from shop.models import *

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(shopping_cart)
admin.site.register(Admin_detail)