from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from geopy import units, distance
from django.urls import reverse
from django.utils import timezone

from .models import Trip, Meetup, Passenger
from django.db.models import Count
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, timedelta

MAX_PASSENGERS = 4
ALLOWABLE_DIST = 0.4

def index(request):
    all_trips = Trip.objects.filter(date__date=datetime.today().date()).annotate(avail_passengers=MAX_PASSENGERS-Count('passenger')).order_by('avail_passengers')
    context = {'trips': all_trips}
    return render(request, 'discover/discover.html', context)

def refreshtrips(request):
    all_trips = Trip.objects.annotate(avail_passengers=MAX_PASSENGERS - Count('passenger'))
    context = serializers.serialize('json', list(all_trips))
    return JsonResponse(context)

def join(request):
    trip_id = request.POST.get('trip_id')
    passenger = request.POST.get('passenger')

    join_trip = Trip.objects.get(pk=trip_id)
    new_passenger = Passenger(trip=join_trip, name=passenger)
    new_passenger.save()

    return HttpResponse(trip_id + " " + passenger)

def organize(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    lat = float(latitude)
    long = float(longitude)
    distance_range = float(ALLOWABLE_DIST)

    rough_distance = units.degrees(arcminutes=units.nautical(kilometers=distance_range)) * 2

    all_meetup_pts = Meetup.objects.filter(latitude__range=(lat - rough_distance, lat + rough_distance), longitude__range=(long - rough_distance, long + rough_distance))

    nearby = []
    for meetup_pt in all_meetup_pts:
        if meetup_pt.latitude and meetup_pt.longitude:
            exact_distance = distance.distance(
                (lat, long),
                (meetup_pt.latitude, meetup_pt.longitude)
            ).kilometers

            if exact_distance <= distance_range:
                meetup_pt.distance = exact_distance
                nearby.append(meetup_pt)

    sorted(nearby, key=lambda m: m.distance)

    # nearby_meetups = Meetup.objects.filter(id__in=[l.id for l in nearby])

    context = { 'nearby_meetups': nearby }
    return render(request, 'discover/organize.html', context)

def createTrip(request):
    organizer = request.POST.get('organizer')
    selected_meetup = request.POST.get('choice')

    new_meetup = get_object_or_404(Meetup, pk=selected_meetup)

    new_trip = Trip(meetup_pt=new_meetup, organizer=organizer, date=timezone.now() + timedelta(hours=9))
    new_trip.save()

    new_passenger = Passenger(trip=new_trip, name=organizer)
    new_passenger.save()

    return HttpResponseRedirect(reverse('discover:index'))