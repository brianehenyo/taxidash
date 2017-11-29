from django.db import models
from datetime import datetime

class Meetup(models.Model):
    latlong = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Trip(models.Model):
    meetup_pt = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    organizer = models.CharField(max_length=200)
    date = models.DateTimeField('date organized', default=datetime.now)

    def __str__(self):
        return self.organizer

class Passenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

