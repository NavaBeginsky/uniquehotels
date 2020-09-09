from django import forms
# from .models import Categories, Amenities

# class CategoryForm(forms.Form):
#     category_options = Categories.objects.all().values_list('pk', 'name')
#     categories = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         choices=category_options
#     )

# class AmenityForm(forms.Form):
#     amenity_options = Amenities.objects.all().values_list('pk', 'name')
#     amenities = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         choices=amenity_options
#     )

# class LocationForm(forms.Form):
#     lat = forms.FloatField(required=False)
#     lon = forms.FloatField(required=False)
#     radius = forms.IntegerField(required=False)

#     def __init__(self, *args, **kwargs):
#         super(LocationForm, self).__init__(*args, **kwargs)
#         self.fields['radius'].label = "Kilometers"