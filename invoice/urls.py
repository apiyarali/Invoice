from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
    path("customer/<int:cust_id>/invoice", views.invoice_form, name="invoice_form"),
    path("customer", views.customer, name="customer"),
    path("add-customer", views.add_customer, name="add_customer"),
    path("customer/<int:cust_id>/edit", views.edit_customer, name="edit_customer"),
    path("products", views.products, name="products"),
    path("add-product", views.add_product, name="add_product"),
    path("create-invoice", views.create_invoice, name="create_invoice"),
    path("invoice/<int:inv_id>", views.invoice_view, name="invoice_view"),
    path("pdf/<int:inv_id>", views.pdf, name="pdf")
]