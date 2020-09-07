from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .forms import AddHotelForm, HotelPhotosForm, ContactForm
from hotels.models import HotelPhotos, Country, Location
from . import models
from django.contrib import messages
from django.forms.models import modelformset_factory


# Create your views here.
def addHotel(request):
    imageFormSet = modelformset_factory(
        HotelPhotos, 
        form=HotelPhotosForm, 
        extra=5
        )
    if request.method == 'POST':
        hotel_form = AddHotelForm(request.POST)
        photos_formset = imageFormSet(request.POST, request.FILES)
        if hotel_form.is_valid() and photos_formset.is_valid():
            country, created = Country.objects.get_or_create(name = hotel_form.cleaned_data['country'])
            location, created = Location.objects.get_or_create(city=hotel_form.cleaned_data['city'], country=country)
            hotel = hotel_form.save(commit=False)
            hotel.location = location
            hotel.approved = False
            hotel.save()

            images = photos_formset.save(commit=False)
            print(photos_formset)
            for image in images:
                image.hotel = hotel
                image.save()

            for category in hotel_form.cleaned_data['categories']:
                hotel.categories_set.add(category)
            
            for amenity in hotel_form.cleaned_data['amenities']:
                hotel.amenities_set.add(amenity)

            messages.success(request, 'Form submission successful')
            
    context = {
        'form': AddHotelForm,
        'photos_formset': imageFormSet(queryset=HotelPhotos.objects.none())
    }
    return render(request, 'contact/addhotel.html', context)

class Contact(SuccessMessageMixin, generic.CreateView):
    model = models.Contact
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_message = 'Form submission successful!'
    
    def get_success_url(self):
        return self.request.path