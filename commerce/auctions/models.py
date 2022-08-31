from django.contrib.auth.models import AbstractUser
from django.db import models

# Register your models here.

class User(AbstractUser):
    pass

class Listings(models.Model):
    user = models.ForeignKey(User, blank=False,on_delete=models.CASCADE , related_name="posted_by")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    initial_value = models.IntegerField()
    image_link = models.CharField(max_length=1000)

class Bid(models.Model):
    item = models.ManyToManyField(Listings, blank=True, related_name="bid_item")
    value = models.IntegerField()
    user = models.ManyToManyField(User, blank=False, related_name="user_bid")

class Comments(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="user_coment")
    comment = models.CharField(max_length=1000)
    listing = models.ManyToManyField(Listings, blank=False, related_name="comented_listings")
