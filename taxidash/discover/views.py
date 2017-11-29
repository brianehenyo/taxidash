from django.shortcuts import render

from django.http import HttpResponse

from .models import Trip


def index(request):
    all_trips = Trip.objects.all()
    context = {'trips': all_trips}
    return render(request, 'discover/discover.html', context)

def detail(request):
    return HttpResponse("Hello, world. You're at a trip's detail.")
