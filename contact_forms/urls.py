from django.urls import path
from . import views

urlpatterns = [
    path('addhotel/', views.addHotel, name='addhotel'),
    path('contact/', views.Contact.as_view(), name='contact')
]