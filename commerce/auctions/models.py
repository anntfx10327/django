from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Action(models.Model):
    item_name = models.CharField(max_length=100, null=True)
    item_description = models.TextField(max_length=1000, null=True)
    image_url = models.CharField(max_length=1000, null=True)
    category = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=100, null=True, blank=True)
    seller = models.CharField(max_length=100, null=True)#, editable=True) co the sua

    def __str__(self):
        return f"{self.item_name}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)
    listing = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="listing_bids", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ('-bid_time',)

    def __str__(self):
        return f"{self.user} put a bid in for {self.price}"


class Comment(models.Model):
    listing = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="listing_comments", null=True)
    time    = models.DateTimeField(auto_now_add=True, null=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    message = models.TextField(max_length=500, null=True)
    
    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"


class Wish(models.Model):
    user = models.CharField(max_length=64, null=True, blank=True)
    listing_id = models.IntegerField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"