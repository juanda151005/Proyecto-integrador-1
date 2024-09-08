from django.shortcuts import render
from .models import Reviews

def reviews(request):
    reviewss = Reviews.objects.all().order_by('-general_rate')
    return render(request, 'reviews.html', {'reviewss':reviewss})
