This Django app is for generating invoices for customers along with a product database and client database.

Users can add their own profile and client profile which will show on the invoice.

Users can also add products which will allow users to select products from the dropdown list when creating an invoice.

The app also allows converting invoices into PDF for emailing it to customers and marking invoices as paid when customer has paid.

Before running the app, make migrations (python manage.py makemigrations) and add your Django secret key under settings. To access the admin panel create superuser (python manage.py createsuperuser).