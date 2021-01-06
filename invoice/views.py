import json
import pytz
import pdfkit
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime


from .models import User, Customer, Invoice, Profile, AbstractAddressModel, Product, Item
from . import forms, util


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    invoices = Invoice.objects.filter(user=request.user).order_by('-dueDate')

    return render(request, "invoice/index.html",{
        "organization": util.getOrganization(request.user),
        "invoices": invoices
    })

def login_view(request):
    if request.method == "POST":
    
        # User sign in attempt
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Authenticate user
        if user is not None:
            login(request, user)
            return redirect("index")
            # return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "invoice/login.html", {
                "message": "Invalid email and/or password."
            })  
    else:
        return render(request, "invoice/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        
        # Get form data
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password match
        if password != confirmation:
            return render(request, "invoice/register.html", {
                "message": "Passwords must match."
            })
        
        # Create new user
        try:
            user = User.objects.create_user(email, email, password, first_name=firstName, last_name=lastName)
            user.save()
        except IntegrityError:
            return render(request, "invoice/register.html", {
                "message": f"User with email {email} already exist."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "invoice/register.html")
        
@login_required(login_url="login")
def profile(request):

    # Get profile if exist else return none
    profile = Profile.objects.filter(user=request.user).first()

    # Pre-fill form if profile exist
    form = forms.ProfileForm(instance=profile)

    # Save changes
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            uform=form.save(commit=False)
            uform.user = request.user
            uform.save()
            return redirect("profile")

    return render(request, "invoice/profile.html", {
        "form": form,
        "organization": util.getOrganization(request.user)
    })

# Customer List
@login_required(login_url="login")
def customer(request):
    customers = Customer.objects.filter(user=request.user).order_by('firstName')

    return render(request, "invoice/customer.html",{
        "customers": customers,
        "organization": util.getOrganization(request.user)
    })

# Add Customer
@login_required(login_url="login")
def add_customer(request):

    if request.method == "POST":

        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            nform=form.save(commit=False)
            nform.user = request.user
            nform.save()
            return redirect("customer")

    return render(request, "invoice/add-customer.html",{
        "form": forms.CustomerForm,
        "organization": util.getOrganization(request.user),
    })

# Edit Customer Data
@login_required(login_url="login")
def edit_customer(request, cust_id):
    customer = get_object_or_404(Customer, id=cust_id)

    # Check if customer was added by the logged in user
    if request.user != customer.user:
        messages.error(request, "Not authorize to edit this customer")
        return redirect("customer")
    
    # Pre-fill customer form, if customer exists.
    form = forms.CustomerForm(instance=customer)
    if request.method == "POST":
        form = forms.CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            ceform=form.save(commit=False)
            ceform.user = request.user
            ceform.save()
            return redirect("customer")
    
    return render(request, "invoice/edit-customer.html", {
        "form": form,
        "organization": util.getOrganization(request.user),
        "cust_id": cust_id    
    })

# Invoice Form (doesn't create invoice)
@login_required(login_url="login")
def invoice_form(request, cust_id):
    profile = get_object_or_404(Profile, user=request.user)

    # Check if customer exists
    try:
        customer = get_object_or_404(Customer, id=cust_id)
    except:
        messages.error(request, "Customer doesn't exists")
        return redirect("customer")

    # Check if customer was added by the logged in user
    if customer.user != request.user:
        messages.error(request, "Not authorize to create invoice for this customer")
        return redirect("customer")   

    # Check to ensure logged in user have products
    try:
        products = get_list_or_404(Product, user=request.user)
    except:
        messages.error(request, "No products exists")
        return redirect("products")    

    # Get minimum date for date input field
    minDate = datetime.today().date().strftime("%Y-%m-%d")

    # Send all product created by user for javascript parse when creating invoice
    products_data = {}

    for product in products:
        products_data[product.id] = product.serialize()

    return render(request, "invoice/invoiceForm.html",{
        "customer": customer,
        "organization": util.getOrganization(request.user),
        "profile": profile,
        "products": products,
        "products_data": products_data,
        "minDate": minDate
    })

# Product List
@login_required(login_url="login")
def products(request):

    products = Product.objects.filter(user=request.user)

    return render(request, "invoice/products.html",{
        "products": products,
        "organization": util.getOrganization(request.user), 
    })

# Add Product API
@login_required(login_url="login")
def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pname = data.get("productName")
        pamount = data.get("amount")

        if not pname or not pname.strip:
            return JsonResponse({"error": "Product Name Required"}, status=400)
        elif float(pamount) <= 0:
            return JsonResponse({"error": "Amount must be greater than zero"}, status=400)    
        else:
            product = Product(
                user=request.user, 
                productName=data.get("productName"),
                productDescription=data.get("productDescription"),
                rate=float(data.get("amount"))
            )
            product.save()
            return JsonResponse({"success": "procuct has been added"}, status=200)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)

# Create Invoice API
@login_required(login_url="login")
def create_invoice(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Calculate invoice total 
        linesTotal = 0
        for items in data.get("lineItems"):
            pId = items["productID"]
            product = Product.objects.get(id=pId)
            pRate = float(product.rate)
            pQty = int(items["productQty"])
            price = pRate*pQty
            linesTotal = linesTotal + price

        # Ensure due date is greater than or equal to today
        dInputDate = data.get("dueDate")
        dDate = datetime.strptime(dInputDate,"%Y-%m-%d").date()
        minDate = datetime.today().date()  
        if not dInputDate:
            return JsonResponse({"error": "Due Date required"}, status=400)
        elif dDate <  minDate:
            return JsonResponse({"error": "Due Date must be greater then or equal to today"}, status=400)

        # Create invoice
        cust = Customer.objects.get(id=data.get("customer"))
        inv = Invoice(
            user=request.user,
            customer=cust,
            dueDate=data.get("dueDate"),
            created=minDate,
            invoiceTotal=linesTotal
        )
        inv.save()

        # Add line items
        for items in data.get("lineItems"):
            prod = Product.objects.get(id=items["productID"])
            lineItems = Item(
                invoice = inv,
                product = prod,
                qty = int(items["productQty"])
            )
            lineItems.save()
        return JsonResponse({"url": reverse("index")}, status=200)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)

# Invoice View (for individual invoice and marking paid)
@login_required(login_url="login")
def invoice_view(request, inv_id):
    profile = get_object_or_404(Profile, user=request.user)
    items = Item.objects.filter(invoice=inv_id)

    # Check if inovice exists
    try:
        invoice = Invoice.objects.get(id=inv_id)
    except:
        messages.error(request, "Invoice doesn't exist")
        return redirect("index")

    # Ensure invoice being accessed was created by logged in user
    if invoice.user != request.user:
        messages.error(request, "Not authorize to view this invoice")
        return redirect("index")   

     # Get minimum date for date input field
    minDate = invoice.created.strftime("%Y-%m-%d")

    # Mark invoice as paid
    if request.method == "POST":
        pInputDate = request.POST.get("paid-date")
        pDate = datetime.strptime(pInputDate,"%Y-%m-%d").date()

        # Ensure paid date is entered and is greater then invoice created date
        if not pInputDate:
            messages.error(request, "Paid Date cannot be empty")
            return redirect("invoice_view", inv_id)
        elif pDate < invoice.created:
            messages.error(request, "Paid Date cannot less than Invoice Date")
            return redirect("invoice_view", inv_id)
        else:
            invoice.paidDate = pDate
            invoice.save()
            return redirect("invoice_view", invoice.id)
            
    return render(request, "invoice/invoiceView.html",{
        "items": items,
        "profile": profile,
        "invoice": invoice,
        "organization": util.getOrganization(request.user),
        "minDate": minDate
    })

# Generate PDF
# Code snippet for this is taken form:
# https://ourcodeworld.com/articles/read/241/how-to-create-a-pdf-from-html-in-django
# This function require installing pdfkit (pip install pdfkit) and 
# wkhtmltopdf (https://wkhtmltopdf.org/downloads.html) or ($ sudo apt-get install wkhtmltopdf)
@login_required(login_url="login")
def pdf(request, inv_id):

    options = {
        'cookie': [('sessionid', request.COOKIES['sessionid'])],
        }

    # Create a URL of our project and go to the template route
    projectUrl = request.get_host() + reverse("invoice_view", args=[inv_id])
    pdf = pdfkit.from_url(projectUrl, False , options=options)

    # Generate download
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response