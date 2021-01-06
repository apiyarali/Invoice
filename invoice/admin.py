from django.contrib import admin
from .models import User, Customer, Invoice, Profile, AbstractAddressModel, Product, Item

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Profile)
admin.site.register(Item)
