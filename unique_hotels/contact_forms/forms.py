from django import forms
from hotels import models
from .models import Contact
from mapwidgets.widgets import GooglePointFieldWidget


class AddHotelForm(forms.ModelForm):
    class Meta:
        model = models.Hotels
        fields = ['name', 'unique_snippet', 'point_coordinates', 'details', 'booking_website', 'contact_email']
        labels = {
            'name': 'Hotel name',
            'point_coordinates': 'Location on map'
        }
        widgets = {
            'point_coordinates': GooglePointFieldWidget,
            'unique_snippet': forms.Textarea(attrs={
                'cols': 60, 
                'rows': 2, 
                'placeholder': 'What makes this hotel unique?'
                }),
            'details': forms.Textarea(attrs={'cols': 60, 'rows': 15})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        possible_categories = models.Categories.objects.all() 
        self.fields['categories'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=possible_categories,
            required=False)
        possible_amenities = models.Amenities.objects.all()
        self.fields['amenities'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=possible_amenities,
            required=False)
        self.fields['city'] = forms.CharField(max_length=100)
        self.fields['country'] = forms.CharField(max_length=50)
        

class HotelPhotosForm(forms.ModelForm):
    class Meta:
        model = models.HotelPhotos
        fields = ['image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'subject': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'details': forms.Textarea(attrs={'cols': 50, 'rows': 10})
        }