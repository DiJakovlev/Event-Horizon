import random

from django.db import models
from user.forms import UserRegisterForm


class Event(models.Model):
    event_id = models.CharField(null=False, blank=False, default=None)
    name = models.TextField(null=False, blank=False, max_length=999)
    summary = models.CharField(null=False, blank=False, max_length=140)
    description = models.TextField(null=False, blank=False, max_length=999)
    url = models.URLField(null=False, blank=False, max_length=512)
    start_date = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    currency = models.CharField(null=False, blank=False, max_length=140)
    online_event = models.BooleanField(null=False, blank=False)
    listed = models.BooleanField(null=False, blank=False)
    shareable = models.BooleanField(null=False, blank=False)
    capacity = models.IntegerField(null=True, blank=True, default=random.randint(5, 40))
    event_logo = models.ImageField(null=False, blank=False, default='No logo provided', max_length=512)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegisterForm, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - {self.user.name}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(UserRegisterForm, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return f"{self.user.name}'s shopping cart"
