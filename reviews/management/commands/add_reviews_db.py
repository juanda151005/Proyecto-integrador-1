from django.core.management.base import BaseCommand
from reviews.models import Reviews
import os
import json

class Command(BaseCommand):
    help = 'Load reviews from reviews.json into the Review model'

    def handle(self, *args, **kwargs):
        json_file_path = 'reviews/management/commands/reviews.json'

        with open(json_file_path, 'r') as file:
            reviews = json.load(file)

        for i in range(len(reviews)):
            review = reviews[i]
            exist = Reviews.objects.filter(city=review['city'], general_review=review['general_review']).first()
            if not exist:
                Reviews.objects.create(
                    city=review['city'],
                    general_review=review['general_review'],
                    touristic_places_rate=review['touristic_places_rate'],
                    history_and_culture_rate=review['history_and_culture_rate'],
                    gastronomy_rate=review['gastronomy_rate'],
                    costs_rate=review['costs_rate'],
                    safety_rate=review['safety_rate'],
                    weather_rate=review['weather_rate'],
                )
                