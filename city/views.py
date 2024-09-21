from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from reviews.models import Reviews
from .models import City

def home(request):
    searchTerm=request.GET.get('searchCity')
    if searchTerm:
        cities = City.objects.filter(name__icontains=searchTerm)
    else:  
        cities=City.objects.all()
    cities = cities.order_by('-rate')
    return render(request, 'home.html', {'searchTerm': searchTerm, 'cities': cities})

def city(request):
    searchTerm=request.GET.get('searchCity')
    if searchTerm:
        cities = City.objects.filter(name__icontains=searchTerm)
    else:  
        cities=City.objects.all()
    cities = cities.order_by('-rate')
    return render(request, 'city.html', {'searchTerm': searchTerm, 'cities': cities})

def city_reviews(request, city_name):
    city = get_object_or_404(City, name=city_name)
    reviews = Reviews.objects.filter(city=city.name)

    context = {
        'city': city,
        'reviews': reviews
    }
    
    return render(request, 'city_reviews.html', context)