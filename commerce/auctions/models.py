from django.contrib.auth.models import AbstractUser
from django.db import models

# Register your models here.

class User(AbstractUser):
    def __str__ (self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ('name')

    def __str__():
        return f"{self.name}"

    @property
    def count_active_auctions(sefl):
        return Listings.objects.filter(category=self).count()

class Listings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name="auctions")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    initial_value = models.IntegerField(max_digits=7, decimal_places=2)
    image = models.ImageField(blank=True,null=True, upload_to="")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="auctions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    durations= (
        (1, "one day")
        (3, "Three days")
        (7,"one week")
        (14, "two weeks")
    )
    duration = models.IntegerField(choices=durations)



class Bid(models.Model):
    item = models.ForeignKey(Listings, blank=False, on_delete=models.CASCADE, related_name="bid_item")
    value = models.IntegerField()
    user = models.ForeignKey(User, blank=False,on_delete = models.CASCADE, related_name="user_bid")

class Comments(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="user_coment")
    comment = models.CharField(max_length=1000)
    listing = models.ManyToManyField(Listings, blank=False, related_name="comented_listings")
