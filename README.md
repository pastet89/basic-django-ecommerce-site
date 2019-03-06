# Django-based simplified grocery e-commerce website with Docker support

Contains admin panel from which can be created nested categories
and added/updates products with images. The user can view the 
products within a category, add products to cart and edit the cart.
The checkout process simply clears the cart session. The front-end functionality
is based on jQuery. The website can be run using the Django's
built-in test server, or in a Docker container using Nginx and Gunicorn.

## Requirements:

* Python 3.6+
* MySQL 5.5+
* Additional Python packages, specified in requirements.txt 

## Installation:

1. Install the MySQL database running ```eshop/db.sql```:
```
$ mysql -u user -p
mysql> USE `DB_NAME`;
mysql> source eshop/db.sql;
```
2. Install the required packages:
```
pip3 install -r requirements.txt
```
3. Enter your MySQL connection details in ```eshop/eshop/settings.py```. The default values you will find there
are used inside the Docker container, hence the ```db``` value for the database host. Feel free to change them
to whatever you need and just keep in mind you will need to use those settings in case you wish to run the app in the 
Docker container.

## Usage:

Add or edit categories and products from the admin panel. The website
uses the default Django admin app, located at ```YOUR_HOST/admin```.
You can login with user ```admin``` and password ```EbagAdmin123```.
From the project folder ```eshop/``` run the Django test server:
```
python3 manage.py runserver
```
Browse the website at ```127.0.0.1:8000```, add items to cart and checkout.

## Tests:

Run the unit tests from the project folder ```eshop/``` using:
```
python3 manage.py test --nomigrations
```
The ```--nomigrations``` flag is used to avoid a strange problem related the creation of a migrations table
during the tests. For this reason ```django-test-without-migrations``` is used.

## Running the app in a Docker container

The app by default uses the Django test server, however, you can also run it using Nginx and Gunicorn
in a Docker container if you have installed [docker-compose](https://docs.docker.com/compose/install/). 
To do so:
1. Collect the static files. From the project folder ```eshop/``` run:
```
python3 manage.py collectstatic --no-input
```
2. Make sure that the database settings in ```eshop/eshop/settings.py``` are as follows:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PASSWORD': 'eshop_pass',
        'USER': 'eshop_user',
        'NAME': 'eshop',
        'HOST': 'db',
    }
}
``` 
3. Build the Docker images and create the containers. There are three containers: 
one for the Django app and Gunicorn, one for MySQL and one for Nginx.
From the ```docker/``` folder run:
```
docker-compose up -d
```
This will take a while (a few minutes as all images and dependencies need to be
downloaded, built and installed).
You might need to wait a few seconds after that before the database becomes available and you can run the app.
4. You can now open the app in the browser at ```http://localhost:8000```
5. Running tests in the Docker container. From the ```docker/``` folder run:
```
docker-compose exec djangoapp sh -c 'cd /opt/services/djangoapp/eshop && python manage.py test --nomigrations'
```
Please, note that ```/opt/services/djangoapp``` is the location of the app root folder inside the container.
This path is set from the Docker environment variable ```DJANGOAPP_CONTAINER_ROOT_DIR``` in the ```docker/.env``` file.
6. To stop the containers run:
```
docker-compose stop
```
7. To stop and remove the containers run:
```
docker-compose down
```

### Notes:

The website uses a free template from [Colorlib](https://colorlib.com/).
The jQuery web app funcionality is located in ```eshop/ebag/static/js/main.js```.
The ```test-img.png``` in the ```eshop/ebag/static/images``` folder
is used by the unit tests and must be present in that location.
