from django.db import models


class Event(models.Model):
    name = models.TextField(null=False, blank=False, max_length=999)
    summary = models.CharField(null=False, blank=False, max_length=140)
    description = models.TextField(null=False, blank=False, max_length=999)
    url = models.URLField(null=False, blank=False)
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    currency = models.CharField(null=False, blank=False, max_length=140)
    online_event = models.BooleanField(null=False, blank=False)
    listed = models.BooleanField(null=False, blank=False)
    shareable = models.BooleanField(null=False, blank=False)
    invite_only = models.BooleanField(null=False, blank=False)
    show_remaining = models.BooleanField(null=False, blank=False)
    password = models.CharField(null=True, blank=True, max_length=100)
    capacity = models.IntegerField(null=False, blank=False)





