from django.db import models

# Create your models here.

class Addproduct(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=100)
    product_price = models.CharField(max_length=100)
    product_offerprice = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="image")

    class Meta:
        db_table:"Addproduct"

class Addcart(models.Model):
    producti_id = models.CharField(max_length=100)
    producti_name = models.CharField(max_length=100)
    producti_price = models.CharField(max_length=100)
    producti_category = models.CharField(max_length=100)
    image = models.ImageField(upload_to=100)
    producti_qty = models.CharField(max_length=100)
    totalprice = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    class Meta:
        db_table:"Addcart"

class Payment(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    class Meta:
        db_table:"Payment"

class Wishlist(models.Model):
    product_id = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to="image") 
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_price = models.CharField(max_length=100)
    product_offerprice = models.CharField(max_length=100)
    
    username =  models.CharField(max_length=100)

    class Meta:
        db_tatble:"Wishlist"