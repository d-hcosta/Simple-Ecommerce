
# Simple E-commerce

This is a small (still incomplete) e-commerce project made with Django and Python, focused on the backend.


## This project does not yet include:

 - Shopping cart discount coupons.
 - Freight calculation.
 - Payment methods.

## Goals

- [x]  Listing and details of products and variations
- [x]  Session-based shopping cart
- [x]  Remove products from cart
- [x]  Model profile (create and update)
- [x]  Model products and variations
- [x]  Payment page
- [x]  Register customer order
- [x]  Customer Login and Logout

## Installation

Below is a list of commands to clone and configure this project on your local machine:
### Downloading the repository:
```
git clone https://github.com/Vrag404/Simple-Ecommerce.git
```

### Windows:
```
cd Simple-Ecommerce
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
```
### Linux:
```
cd Simple-Ecommerce
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```    

## Screenshot:
![image](https://user-images.githubusercontent.com/88698720/162589993-c0a8b79f-b435-4b7c-875e-923dfb708f34.png)
