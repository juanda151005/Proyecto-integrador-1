from django.shortcuts import render
from django.http import HttpResponse

from .models import City

# Create your views here.

def home(request):
    #return render(request, 'home.html')
    searchTerm=request.GET.get('searchCity')
    if searchTerm:
        cities = City.objects.filter(name__icontains=searchTerm)
    else:  
        cities=City.objects.all()
    cities = cities.order_by('-rate')
    return render(request, 'home.html', {'searchTerm': searchTerm, 'cities': cities})
