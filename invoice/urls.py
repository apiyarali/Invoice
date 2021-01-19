from django.urls import path, include, re_path
from django.views.generic import RedirectView

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
    path("pdf/<int:inv_id>", views.pdf, name="pdf"),

    # django all-auth

    # re_path to redirect or block django all-auth other urls such as sign up, password reset,
    # etc. As this app has custom signup forms.
    # django all-auth is only for loggin in with google, otherwise user will have to use custom
    # in-app registration form.

    re_path(r'^accounts/$', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/\s', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/signup/$', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/login/$', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/password.', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/inactive.', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/email.', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/confirm-email.', RedirectView.as_view(pattern_name='index', permanent=False)),
    re_path(r'^accounts/social.', RedirectView.as_view(pattern_name='index', permanent=False)),
    path('accounts/', include('allauth.urls')), 
]
