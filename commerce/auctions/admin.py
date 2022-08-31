from curses.ascii import US
from django.contrib import admin
from .models import Comments,Bid,User,Listings

admin.site.register(User)

admin.site.register(Comments)
admin.site.register(Bid)
admin.site.register(Listings)


