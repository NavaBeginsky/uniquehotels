from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.show_hotels, name = 'show_hotels'),
]