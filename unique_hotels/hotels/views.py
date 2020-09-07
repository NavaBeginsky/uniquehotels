from django.shortcuts import render, redirect
from .models import Hotels, HotelPhotos
from random import choice
from django.contrib.auth.decorators import login_required
from users import models
from .forms import CategoryForm, AmenityForm, LocationForm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

# Create your views here.
def filter_hotels(hotels, *args):
    filtered_hotels = hotels #needs to be assigned in order for the forloop assignment to be able to be passed back
    for category in args[0]:
        filtered_hotels = filtered_hotels.filter(categories=category) 

    for amenity in args[1]:
        filtered_hotels = filtered_hotels.filter(amenities=amenity) 

    if args[2] and args[3] and args[4]:
        location = GEOSGeometry(f'POINT({args[3]} {args[2]})')#points are long/lat and get location is lat/long, so it has to be reversed
        filtered_hotels = filtered_hotels.filter(point_coordinates__distance_lte=(location, D(km=(args[4]))))
        print(type(args[4]))

    if len(filtered_hotels) == 0: 
            return False

    return filtered_hotels


def choose_hotel(current_user, *args):
    if current_user.is_authenticated:
        unjudged_hotels = Hotels.objects.exclude(liked_by_user=current_user).exclude(
            rejected_by_user=current_user).exclude(approved=False)
        if len(unjudged_hotels) == 0:  # if the user has judged all the hotels on the site
            return False
    else:
        unjudged_hotels = Hotels.objects.exclude(approved=False)

    filtered_hotels = filter_hotels(unjudged_hotels, *args)
    if filtered_hotels == False: 
            return False
        
    return choice(filtered_hotels)


def show_hotels(request):
    current_user = request.user
    if request.method == 'POST':
        if current_user.is_authenticated:
            hotel = Hotels.objects.get(pk=request.POST.get('hotel_pk'))
            if 'like' in request.POST:
                current_user.liked.add(hotel)
            if 'reject' in request.POST:
                current_user.rejected.add(hotel)

        elif 'skip' not in request.POST:  # user should be able to skip through hotels even if not logged in
            return redirect('login')
    
    locationForm = LocationForm(request.GET)
    if locationForm.is_valid():#the only form that takes a user input so it needs to be cleaned
        if 'lat' in request.GET and 'radius' in request.GET:
            lat = locationForm.cleaned_data['lat']
            lon = locationForm.cleaned_data['lon']
            distance = locationForm.cleaned_data['radius']
        else:
            lat, lon, distance = None, None, None
    chosen_hotel = choose_hotel(current_user, request.GET.getlist('categories'), request.GET.getlist('amenities'), lat, lon, distance)
    
    context = {
        'hotel': chosen_hotel,
        'cat_form': CategoryForm(request.GET),
        'amen_form': AmenityForm(request.GET),
        'dist_form': LocationForm(request.GET)
    }

    if chosen_hotel == False:
        return render(request, 'hotels/nohotels.html', context)

    return render(request, 'hotels/showhotels.html', context)
