from django.contrib import admin
from .models import User, NewListing, UserWatchlist, UserComments, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(NewListing)
admin.site.register(UserWatchlist)
admin.site.register(UserComments)
admin.site.register(Bid)
