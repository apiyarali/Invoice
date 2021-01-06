from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from decimal import Decimal

class User(AbstractUser):
    pass

class AbstractAddressModel(models.Model):
    phone = models.CharField("Phone Number", max_length=255, blank=True)
    organization = models.CharField("Business Name", max_length=255, blank=True)
    address1 = models.CharField("Address 1", max_length=255, blank=True)
    address2 = models.CharField("Address 2", max_length=255, blank=True)
    city = models.CharField("City", max_length=255, blank=True)
    province = models.CharField("Province/State", max_length=255, blank=True)
    zipCode = models.CharField("Zip/Postal Code", max_length=255, blank=True)
    country = models.CharField("Country", max_length=255, blank=True)
    created = models.DateTimeField(default=datetime.now(), blank=True)

    class Meta:
        abstract = True

class Profile(AbstractAddressModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
   
    def serialize(self):
        return{
            "id": self.id,
            "email": self.user.email,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "company": self.organization,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "province": self.province,
            "country": self.country
        }

class Customer(AbstractAddressModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    firstName = models.CharField("First Name", max_length=255, blank=False)
    lastName = models.CharField("Last Name", max_length=255, blank=False)
    email = models.EmailField("Email Address", blank=False)

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "email": self.email,
            "company": self.organization,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "province": self.province,
            "country": self.country
        }
    
    def full_name(self):
        return f"{self.firstName} {self.lastName}"

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
    customer =  models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customerInvoice")
    invoiceTotal = models.DecimalField(max_digits=6, decimal_places=2, blank=True) 
    created = models.DateField(blank=True)
    paidDate = models.DateField(blank=True, null=True)
    dueDate = models.DateField(blank=False)

    def serialize(self):
        return{
            "user": self.user.username,
            "customer": self.customer.firstName, 
            "invoiceTotal": self.invoiceTotal,
            "created":self. created,            
            "dueDate": self.dueDate,
            "paidDate": self.paidDate
        } 

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    productName = models.CharField("Product Name", max_length=255, blank=False)
    productDescription = models.CharField("Product Description", max_length=255, blank=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    created = models.DateTimeField(default=datetime.now(), blank=True)

    def serialize(self):
        return{
            "user": self.user.username,
            "productName": self.productName,
            "productDescription": self.productDescription,
            "rate":self.rate   
        }

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoiceItems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productItems")
    qty = models.IntegerField("Quantity", default=1)

    def price(self):
        return self.product.rate*self.qty