from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='city/images/')

    def __str__(self):
        return self.name
