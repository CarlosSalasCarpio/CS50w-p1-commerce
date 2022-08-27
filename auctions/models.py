from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionListingModel(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=64)
    image = models.URLField(max_length=200, blank=True)
    auction_open = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True)
    watchlist = models.ManyToManyField(User, related_name='watchlist')

class bidsModel(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(auctionListingModel, on_delete=models.CASCADE, related_name='bid')

class commentsModel(models.Model):
    comment = models.CharField(max_length=280)
    auction = models.ForeignKey(auctionListingModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)