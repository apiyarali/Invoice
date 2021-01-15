from django import forms
from django.forms import ModelForm
from .models import User, Customer, Invoice, Profile, AbstractAddressModel, Product

# Reference / code-snippet for BaseForm taken from :
# https://riptutorial.com/django-forms/example/27777/add-custom-css-classes
# modified as needed

# Form Inheritance: https://chriskief.com/2013/06/30/django-form-inheritance/
# and https://www.pydanny.com/overloading-form-fields.html


# Base form to apply bootstrap form-control class
class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# User Register Form
# class RegisterForm(forms.BaseForm):
#     class Meta:
#         model = User
#         fields=["firstName", "lastName", "Email", "password1", "password2"]
#         widgets = {
#             "firstName": forms.TextInput(attrs={"placeholder":"First Name"}),
#             "lastName": forms.TextInput(attrs={"placeholder":"Last Name"}),
#             "email": forms.EmailInput(attrs={"placeholder":"Email Address", "pattern":"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"}),
#         }


# Address form templete to be use for profile and customer forms
class AbstractAddressForm(BaseForm):
    class Meta:
        model = AbstractAddressModel
        fields=["phone", "organization", "address1", "address2", "city", "zipCode", "province", "country"]
        widgets = {
            "phone": forms.TextInput(attrs={"type": "tel", "pattern":"[0-9]{3}-[0-9]{3}-[0-9]{4}", "placeholder":"123-456-7890"}),
            "organization": forms.TextInput(attrs={"placeholder":"Company/Organization"}),
            "address1": forms.TextInput(attrs={"placeholder":"Street Address"}),
            "address2": forms.TextInput(attrs={"placeholder":"Apartment/Unit/Suite/Floor"}),
            "city": forms.TextInput(attrs={"placeholder":"City"}),
            "province": forms.TextInput(attrs={"placeholder":"State/Province"}),
            "zipCode": forms.TextInput(attrs={"placeholder":"Zip/Postal Code"}),
            "country": forms.TextInput(attrs={"placeholder":"Country"})
        }

class ProfileForm(AbstractAddressForm):
    class Meta:
        model = Profile
        fields = AbstractAddressForm.Meta.fields
        widgets = AbstractAddressForm.Meta.widgets

class CustomerForm(AbstractAddressForm):
    class Meta:
        model = Customer
        fields=["firstName", "lastName", "email"] + AbstractAddressForm.Meta.fields
        widgets = {
            "firstName": forms.TextInput(attrs={"placeholder":"First Name"}),
            "lastName": forms.TextInput(attrs={"placeholder":"Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder":"Email Address", "pattern":"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"}),
        }
        widgets.update(AbstractAddressForm.Meta.widgets)

