from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass
        

class NewListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=64)
    bid = models.FloatField()
    image_url = models.URLField(max_length=200, blank=True)
    time = models.CharField(max_length=64)
    category = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=64)

    # def __str__(self):
    #     return f'Title: {self.title}\n. Description: {self.text}, with a bid of ${self.bid}. Created on {self.time}.'


class UserWatchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=64, default='')
    text = models.CharField(max_length=64, default='')
    bid = models.FloatField(default=0)
    image_url = models.URLField(max_length=200, blank=True, default='')
    time = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=64, blank=True, default='')



class UserComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    comment = models.CharField(max_length=200)
    time = models.CharField(max_length=64)


class Bid(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      title = models.CharField(max_length=64)
      price = models.FloatField(default=0)  
      message = models.CharField(max_length=64)
      status = models.CharField(max_length=64, default='not_won')
   
    
