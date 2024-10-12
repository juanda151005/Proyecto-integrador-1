from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from reviews.models import Reviews
from .models import *
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
from datetime import datetime
from django.utils import timezone


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

def city_of_the_day(request):
    load_dotenv(".env")
    api_key = os.getenv("openai_apikey")
    client = OpenAI(api_key=api_key)
    today = datetime.now().date()

    # Verificar si ya hay una recomendación para hoy
    recommendation = CityRecommendation.objects.filter(date=today).first()
    if recommendation:
        city = recommendation.city
    else:
        try:
            # Solicitar la ciudad a OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "user", "content": "Dime una ciudad donde haya un evento o celebración hoy en Colombia (SOLO EL NOMBRE DE LA CIUDAD, SIN TILDES Y CON LA PRIMERA EN MAYUSCULA)."}
                ]
            )
            
            # Procesar la respuesta de OpenAI
            city_name = response.choices[0].message.content.strip()
            print(f"Ciudad recomendada por ChatGPT: {city_name}")

            # Buscar la ciudad en la base de datos
            city = City.objects.get(name=city_name)
            
            # Guardar la recomendación del día
            CityRecommendation.objects.create(city=city, date=today)
        except City.DoesNotExist:
            return HttpResponse(f"La ciudad recomendada por OpenAI ({city_name}) no existe en la base de datos.")

    # Renderizar la ciudad del día
    return render(request, 'city_of_the_day.html', {'city': city})
