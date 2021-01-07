This Djanogo app is for generating invoice for customers along with product database and client database. 

Users can add their own profile and client profile which will show on the invoice.

Users can also add products which will allow users to select product from dropdown list when creating an invoice.

The app also allows converting invoices into PDF for emailing it to customers and marking invoice as paid when customer has paid.

Before running the app, make migrations (python manage.py makemigrations) and add your Django secret key under settings. To access the admin panel create superuser (python manage.py createsuperuser).