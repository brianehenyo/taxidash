from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Trip
from django.db.models import Count
from django.http import JsonResponse
from django.core import serializers

MAX_PASSENGERS = 4


def index(request):
    all_trips = Trip.objects.annotate(avail_passengers = MAX_PASSENGERS-Count('passenger'))
    context = {'trips': all_trips}
    return render(request, 'discover/discover.html', context)

def refreshtrips(request):
    all_trips = Trip.objects.annotate(avail_passengers=MAX_PASSENGERS - Count('passenger'))
    context = serializers.serialize('json', list(all_trips))
    return JsonResponse(context)

def join(request):
    trip_id = request.POST.get('trip_id')
    passenger = request.POST.get('passenger')
    return HttpResponse(trip_id + " " + passenger)

def organize(request):
    return HttpResponse("You are about to organize!")
