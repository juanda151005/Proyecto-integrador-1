from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Route(models.Model):
    STATUS_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    cities = models.TextField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #Guarda la fecha y hora en la que se instancio la clase
    estado = models.CharField(max_length=7, choices=STATUS_CHOICES, default='private')

    def __str__(self):
        return self.name
    
    @property
    def cities_list(self):
        if self.cities:
            return self.cities.split(',')
        return []