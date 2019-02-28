# Django-based simplified grocery e-commerce website

Contains admin panel from which can be created nested categories
and added/updates products with images. The user can view the 
products within a category, add products to cart and edit the cart.
The checkout process simply clears the cart session.

## Requirements:

* Python 3.6+
* MySQL 5.5+
* Additional Python packages, specified in requirements.txt 

## Installation:

1. Install the MySQL database running ```db.sql```:
```
$ mysql -u user -p
mysql> USE `DB_NAME`;
mysql> source db.sql;
```
2. Install the required packages:
```
pip3 install -r requirements.txt
```
3. Enter your MySQL connection details in ```my.cnf```


## Usage:

Add or edit categories and products from the admin panel. The website
uses the default Django admin app, located at ```YOUR_HOST/admin```.
You can login with user ```admin``` and password ```EbagAdmin123```.

Browse the website at ```YOUR_HOST```, add items to cart and checkout.

### Tests:

Run the unit tests from the root folder using:
```
python3 manage.py test
```

### Notes:

The website uses a free template from (Colorlib)[https://colorlib.com/].
The JavaScript web app funcionality is located in ```ebag/static/js/main.js```.
The ```test-img.png``` in the ```ebag/static/images``` folder
is used by the unit tests and must be present in that location.
