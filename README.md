# Django E-commerce Project

A Django-based e-commerce web application developed as a learning/project application.

## Features

- User registration with email OTP verification
- User login/logout
- Product category and subcategory browsing
- Product details and multiple images
- Shopping cart
- Order/checkout flow
- Razorpay payment integration
- Order summary
- Basic product and category management

## Technologies

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap
- Django ORM
- Razorpay
- SMTP Email

## Setup

```bash
git clone https://github.com/Renjitha-R-K/django-ecommerce.git
cd django-ecommerce/thretal
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver