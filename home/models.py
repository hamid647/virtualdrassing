from django.db import models
import datetime	
# Create your models here.
class products(models.Model): 
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discription = models.TextField()
    img = models.ImageField(upload_to='images/')
    img2 = models.ImageField(upload_to='images/',null=True,blank=True)
    img3 = models.ImageField(upload_to='images/',null=True,blank=True)
    img4 = models.ImageField(upload_to='images/',null=True,blank=True)
    catagory = models.CharField(max_length=100)
    disable = models.BooleanField(default= False)

class Buyer_info(models.Model):
    Buyer_name = models.CharField(max_length=100)
    product_id = models.IntegerField()
    Product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    time = models.DateTimeField(default=datetime.datetime.now() , editable=False)
    status = models.CharField(max_length=100, default="Ready To Ship")

class contact_message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    time = models.DateTimeField(default=datetime.datetime.now() , editable=False)
    