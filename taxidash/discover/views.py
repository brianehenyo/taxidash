from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from geopy import units, distance
from django.urls import reverse
from django.utils import timezone
from django.template import loader

from .models import Trip, Meetup, Passenger, TaxiCompany
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime, timedelta

MAX_PASSENGERS = 4
ALLOWABLE_DIST = 0.4


def index(request):
    # all_trips = Trip.objects.filter(date__date=datetime.today().date(), status='ACT').annotate(
    #     avail_passengers=MAX_PASSENGERS - Count('passenger')).filter(avail_passengers__lte=4,
    #                                                                  avail_passengers__gt=0).order_by(
    #     'avail_passengers')
    # context = {'trips': all_trips}
    # return render(request, 'discover/discover.html', context)
    request.session['prevPage'] = 'index'

    return render(request, 'discover/discover.html')


def refreshtrips(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    lat = float(latitude)
    long = float(longitude)
    distance_range = float(ALLOWABLE_DIST)

    rough_distance = units.degrees(arcminutes=units.nautical(kilometers=distance_range)) * 2

    all_trips = Trip.objects.filter(date__date=timezone.now() + timedelta(hours=9), status='ACT', meetup_pt__latitude__range=(lat - rough_distance, lat + rough_distance), meetup_pt__longitude__range=(long - rough_distance, long + rough_distance)).annotate(avail_passengers=MAX_PASSENGERS - Count('passenger')).filter(avail_passengers__lte=4, avail_passengers__gt=0).order_by('avail_passengers')

    nearby = []
    for trip in all_trips:
        if trip.meetup_pt.latitude and trip.meetup_pt.longitude:
            exact_distance = distance.distance(
                (lat, long),
                (trip.meetup_pt.latitude, trip.meetup_pt.longitude)
            ).kilometers

            if exact_distance <= distance_range:
                trip.distance = exact_distance
                nearby.append(trip)

    sorted(nearby, key=lambda m: m.distance)

    trip_cards = loader.render_to_string('discover/tripcards.html', {'trips': nearby})
    output_data = {'trip_cards': trip_cards}
    return JsonResponse(output_data)


def taxiList(request):
    taxi_companies = TaxiCompany.objects.all()
    context = {'trip_id': request.session['joined_trip'],
               'referer': request.session['prevPage'],
               'companies': taxi_companies}
    return render(request, 'discover/taxilist.html', context)


def back(request):
    referer = request.session['prevPage']
    trip_id = request.session['joined_trip']

    if "detail" in referer:
        return HttpResponseRedirect(reverse('discover:detail', args=(trip_id,)))
    else:
        return HttpResponseRedirect(reverse('discover:index'))


def enroute(request):
    trip_id = request.session['joined_trip']
    trip = Trip.objects.get(pk=trip_id)
    trip.status = Trip.ENROUTE
    trip.save()

    trip = Trip.objects.get(pk=trip_id)
    passengers = Passenger.objects.filter(trip=trip)

    request.session['joined_trip'] = -1
    request.session['passenger'] = ""

    context = {'trip': trip,
               'passengers': passengers}

    return render(request, 'discover/enroute.html', context)


def detail(request, trip_id):
    # trip = Trip.objects.get(pk=trip_id)
    trip = Trip.objects.get(pk=request.session['joined_trip'])
    passengers = Passenger.objects.filter(trip=trip)

    request.session['prevPage'] = 'detail'

    context = {'trip': trip,
               'passengers': passengers}
    return render(request, 'discover/trip.html', context)


def join(request):
    trip_id = request.POST.get('trip_id')
    passenger = request.POST.get('passenger')

    request.session['passenger'] = passenger

    join_trip = Trip.objects.get(pk=trip_id)
    passengers = Passenger.objects.filter(trip=join_trip)
    if passengers.count() < 4:
        new_passenger = Passenger(trip=join_trip, name=passenger)
        new_passenger.save()

    request.session['joined_trip'] = trip_id

    # passengers = Passenger.objects.filter(trip=join_trip)
    #
    # context = {'trip': join_trip,
    #            'passengers': passengers}

    return HttpResponseRedirect(reverse('discover:detail', args=(trip_id,)))

    # return render(request, 'discover/trip.html', context)


def leave(request):
    # trip_id = request.POST.get('trip_id')
    trip_id = request.session['joined_trip']
    pass_name = request.session['passenger']

    trip = Trip.objects.get(pk=trip_id)
    passenger = Passenger.objects.get(name=pass_name, trip=trip)
    passenger.delete()

    passengers = Passenger.objects.filter(trip=trip)
    if passengers.count() == 0:
        trip.status = Trip.CANCELLED
        trip.save()

    request.session['joined_trip'] = -1

    return HttpResponseRedirect(reverse('discover:index'))


def organize(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    lat = float(latitude)
    long = float(longitude)
    distance_range = float(ALLOWABLE_DIST)

    rough_distance = units.degrees(arcminutes=units.nautical(kilometers=distance_range)) * 2

    all_meetup_pts = Meetup.objects.filter(latitude__range=(lat - rough_distance, lat + rough_distance),
                                           longitude__range=(long - rough_distance, long + rough_distance))

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

    context = {'nearby_meetups': nearby}
    return render(request, 'discover/organize.html', context)


def createTrip(request):
    organizer = request.POST.get('organizer')
    selected_meetup = request.POST.get('choice')

    request.session['passenger'] = organizer

    new_meetup = get_object_or_404(Meetup, pk=selected_meetup)

    new_trip = Trip(meetup_pt=new_meetup, organizer=organizer, date=timezone.now() + timedelta(hours=9))
    new_trip.save()

    new_passenger = Passenger(trip=new_trip, name=organizer)
    new_passenger.save()

    request.session['joined_trip'] = new_trip.id

    # passengers = Passenger.objects.filter(trip=new_trip)
    #
    # context = {'trip': new_trip,
    #            'passengers': passengers}

    return HttpResponseRedirect(reverse('discover:detail', args=(new_trip.id,)))

    # return render(request, 'discover/trip.html', context)
    # return HttpResponseRedirect(reverse('discover:index'))
