from django.db import models
from city.models import City

class Ranking(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.city.name} - Rank {self.rank}'
