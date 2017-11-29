from django.contrib import admin

from .models import Trip, Passenger, Meetup

class MeetupAdmin(admin.ModelAdmin):
    list_display = ('name', 'latlong')

class TripAdmin(admin.ModelAdmin):
    list_display = ('organizer', 'meetup_pt')

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'trip')

admin.site.register(Trip, TripAdmin)
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Passenger, PassengerAdmin)
