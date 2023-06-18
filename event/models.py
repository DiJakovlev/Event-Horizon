from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(null=False, blank=False, default=None)
    start_date = models.CharField(null=False, blank=False, max_length=120)
    address = models.CharField(null=False, blank=False, max_length=250)
    link = models.URLField(null=False, blank=False, max_length=512, unique=True)
    description = models.TextField(null=True, blank=False, max_length=999)
    venue = models.CharField(null=True, blank=False, max_length=250)
    event_logo = models.ImageField(null=False, blank=False, default='No logo provided', max_length=512)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} - {self.user.first_name}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return f"{self.user.first_name}'s shopping cart"
