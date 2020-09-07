# from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('city', 'country')

    def __str__(self):
        return self.city + ', ' + self.country.name

class Hotels(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    point_coordinates = models.PointField()
    unique_snippet = models.CharField(max_length=500)
    details = models.CharField(max_length=2000)
    liked_by_user = models.ManyToManyField(User, related_name='liked')
    rejected_by_user = models.ManyToManyField(User, related_name='rejected')
    booking_website = models.URLField()
    approved = models.BooleanField(default=True)
    contact_email = models.EmailField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'location')
   
class HotelPhotos(models.Model):
    image = models.ImageField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)    

    def __str__(self):
        return self.hotel.name

class Coordinates(models.Model):
    hotel = models.OneToOneField(Hotels, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lon = models.DecimalField(max_digits=10, decimal_places=7)

class Categories(models.Model):
    name = models.CharField(max_length=100)
    hotel = models.ManyToManyField(Hotels, blank=True)
    
    def __str__(self):
        return self.name

class Amenities(models.Model):
    name = models.CharField(max_length=100)
    hotel = models.ManyToManyField(Hotels, blank=True)

    def __str__(self):
        return self.name
