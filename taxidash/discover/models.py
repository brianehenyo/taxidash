from django.db import models
from datetime import datetime

class Meetup(models.Model):
    location = models.TextField('Address', blank=True)
    latitude = models.FloatField('Latitude', blank=True, null=True)
    longitude = models.FloatField('Longitude', blank=True, null=True)
    name = models.TextField('Name', blank=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    ACTIVE = 'ACT'
    CANCELLED = 'CAN'
    ENROUTE = 'ENR'
    STATUS_CHOICE = (
        (ACTIVE, "Active"),
        (CANCELLED, "Cancelled"),
        (ENROUTE, "En Route")
    )
    meetup_pt = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    organizer = models.CharField(max_length=200)
    date = models.DateTimeField('date organized', default=datetime.now)
    status = models.CharField(max_length=3, choices=STATUS_CHOICE, default=ACTIVE)

    def __str__(self):
        return self.organizer

class Passenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
