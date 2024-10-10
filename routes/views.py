from django.shortcuts import render, redirect
from .IA import recomendacionesIA
from .models import Route
from .forms import RouteForm
# Create your views here.

def route(request):
    public_routes=Route.objects.filter(estado='public')
    return render(request, 'Routes.html',{'public_routes': public_routes})

def create_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('Routes.html')  
    else:
        form = RouteForm()
    
    return render(request, 'CreateRoute.html', {'form': form})