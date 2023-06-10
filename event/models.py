from django.db import models


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
    capacity = models.IntegerField(null=True, blank=True, default=0)
    event_logo = models.ImageField(null=False, blank=False, default='No logo provided', max_length=512)
    objects = models.Manager()

    def __str__(self):
        return self.name
