from django.shortcuts import render, redirect, get_object_or_404
from .IA import recomendacionesIA as IA
from .models import Route
from .forms import *
from django.contrib import messages
# Create your views here.

def route(request):
    public_routes=Route.objects.filter(estado='public')
    return render(request, 'Routes.html',{'public_routes': public_routes})

def create_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        form_list=FormRecommendationList(request.POST)
        form_origin_city = FormRecommendationOriginCity(request.POST)
        form_description = FormRecommendationDescription(request.POST)

        ia=IA(request)
        if form.is_valid():
            route = form.save(commit=False)  
            route.user = request.user  
            route.save() 
            return redirect('route')
        
        if form_list.is_valid():
            recommendation1=ia.RecommendCityWithList(form_list.cleaned_data.get('list'))
            return render(request, 'CreateRoute.html', {'recommendation1':recommendation1,'form': form,'form_list':form_list, 'form_origin_city':form_origin_city, 'form_description':form_description})
        
        if form_origin_city.is_valid():
            recommendation2=ia.CreateRouteWithOriginCity(form_origin_city.cleaned_data.get('city'), form_origin_city.cleaned_data.get('time'))
            return render(request, 'CreateRoute.html', {'recommendation2':recommendation2,'form': form,'form_list':form_list, 'form_origin_city':form_origin_city, 'form_description':form_description})

        if form_description.is_valid():
            recommendation3=ia.RecommendCityWithDescription(form_description.cleaned_data.get('description'))
            return render(request, 'CreateRoute.html', {'recommendation3':recommendation3,'form': form,'form_list':form_list, 'form_origin_city':form_origin_city, 'form_description':form_description})
    else:
        form = RouteForm()
        form_list=FormRecommendationList()
        form_origin_city = FormRecommendationOriginCity()
        form_description = FormRecommendationDescription()

    return render(request, 'CreateRoute.html', {'form': form,'form_list':form_list, 'form_origin_city':form_origin_city, 'form_description':form_description})

def user_routes(request):
    routes = Route.objects.filter(user=request.user)
    return render(request, 'DeleteRoute.html', {'routes': routes})

def delete_route(request, name):
    route = get_object_or_404(Route, name=name, user=request.user)
    
    if request.method == 'POST':  
        route.delete()
        messages.success(request, 'Ruta eliminada correctamente.')

    return redirect('user_routes')
