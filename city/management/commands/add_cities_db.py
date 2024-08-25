from django.core.management.base import BaseCommand
from city.models import City
import os
import json

class Command(BaseCommand):
    help = 'Load cities from cities.json into the City model'

    def handle(self, *args, **kwargs):
        json_file_path = 'city/management/commands/cities.json'

        with open(json_file_path, 'r') as file:
            cities = json.load(file)

        for i in range(len(cities)):
            city = cities[i]
            exist = City.objects.filter(name=city['name'], country=city['country']).first()
            if not exist:
                City.objects.create(
                    name=city['name'],
                    country=city['country'],
                    rate=city['rate'],
                    description=city['description'],
                    image='city/images/default.jpg'
                )