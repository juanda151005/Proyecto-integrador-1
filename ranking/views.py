from django.shortcuts import render
from city.models import City

def top_250_cities(request):
    # Obtener las mejores 250 ciudades basadas en la calificación
    top_cities = City.objects.order_by('-rate')[:250]
    return render(request, 'top_250.html', {'top_cities': top_cities})
