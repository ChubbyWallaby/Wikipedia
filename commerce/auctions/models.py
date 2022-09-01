from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta
from django.utils import timezone
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
    def count_active_auctions(self):
        return Listings.objects.filter(category=self).count()

class Listings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name="auctions")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    initial_value = models.IntegerField(max_digits=7, decimal_places=2,validators=[MinValueValidator(0.01))
    image = models.ImageField(blank=True,null=True, upload_to="")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="auctions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ended_manually = models.BooleanField(default=False)

    durations= (
        (1, "one day")
        (3, "Three days")
        (7,"one week")
        (14, "two weeks")
    )
    duration = models.IntegerField(choices=durations)

   def save(self, *args, **kwargs):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(days=self.duration)
        super().save(*args, **kwargs) # call existing save() method

    def is_finshed(self):
        if self.ended_manually or self.end_time < timezone.now():
            return True
        else:
            return False


class Bid(models.Model):
    item = models.ForeignKey(Listings, blank=False, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, blank=False,on_delete = models.CASCADE, related_name="bids")

class Comments(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="commentes")
    comment = models.CharField(max_length=1000)
    time    = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commentes")
