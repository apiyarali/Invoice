This Django app is for generating invoices for customers along with a product database and client database.

Users can add their own profile and client profile which will show on the invoice.

Users can also add products which will allow users to select products from the dropdown list when creating an invoice.

The app also allows converting invoices into PDF for emailing it to customers and marking invoices as paid when customer has paid.

Before running the app:
* Add your Django secret key under settings.py
* Make migrations (python manage.py makemigrations)
* Migrate (python manage.py migrate)
* Create superuser (python manage.py createsuperuser)
* For Google sign-in:
    * Set up Google OAuth Credentials and API from https://console.developers.google.com/
    * Log-in to Django app admin
    * Under Sites add your Domain and Display name
    * Under Social applicaitons:
        * Provider: Google
        * Name: Google API
        * Client id: your id from Google OAuth Credentials
        * Secret key: your secrete key from Google Oauth Credentials
