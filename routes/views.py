from django.shortcuts import render, redirect, get_object_or_404
from .IA import recomendacionesIA as IA
from .models import Route
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
# Create your views here.

def route(request):
    public_routes=Route.objects.filter(estado='public')
    return render(request, 'Routes.html',{'public_routes': public_routes})

def create_route(request):
    recommendation1 = None
    recommendation2 = None
    recommendation3 = None

    if request.method == 'POST':
        form = RouteForm(request.POST)
        form_list=FormRecommendationList(request.POST)
        form_origin_city = FormRecommendationOriginCity(request.POST)
        form_description = FormRecommendationDescription(request.POST)

        ia=IA(request)
        ia_routes_count = Route.objects.filter(name__startswith="ruta con ayuda de ia").count() + 1

        if form.is_valid():
            route = form.save(commit=False)  
            route.user = request.user  
            route.save()
            messages.success(request, 'Ruta creada exitosamente.') 
            return redirect('route')
        
        if form_list.is_valid() and form_list.cleaned_data.get('list'):
            recommendation1 = ia.RecommendCityWithList(form_list.cleaned_data.get('list'))
            Route.objects.create(
                name=f"ruta con ayuda de ia {ia_routes_count}",
                description=recommendation1['description'],  # Aquí se usa la descripción de la IA
                cities=", ".join(recommendation1['cities']),  # Lista de ciudades separadas por comas
                user=request.user
            )
            messages.success(request, 'Ruta generada automáticamente con las recomendaciones de IA.')

            return render(request, 'CreateRoute.html', {
                'recommendation1': recommendation1, 
                'form': form, 
                'form_list': form_list, 
                'form_origin_city': form_origin_city, 
                'form_description': form_description
            })
        
        if form_origin_city.is_valid() and form_origin_city.cleaned_data.get('city'):
            recommendation2 = ia.CreateRouteWithOriginCity(form_origin_city.cleaned_data.get('city'), form_origin_city.cleaned_data.get('time'))
            Route.objects.create(
                name=f"ruta con ayuda de ia {ia_routes_count}",
                description=recommendation2['description'],  # Aquí se usa la descripción de la IA
                cities=", ".join(recommendation2['cities']),  # Lista de ciudades separadas por comas
                user=request.user
            )
            messages.success(request, 'Ruta generada automáticamente con las recomendaciones de IA.')

            return render(request, 'CreateRoute.html', {
                'recommendation2': recommendation2, 
                'form': form, 
                'form_list': form_list, 
                'form_origin_city': form_origin_city, 
                'form_description': form_description
            })

        if form_description.is_valid() and form_description.cleaned_data.get('description'):
            recommendation3 = ia.RecommendCityWithDescription(form_description.cleaned_data.get('description'))
            Route.objects.create(
                name=f"ruta con ayuda de ia {ia_routes_count}",
                description=recommendation3['description'],  # Aquí se usa la descripción de la IA
                cities=", ".join(recommendation3['cities']),  # Lista de ciudades separadas por comas
                user=request.user
            )
            messages.success(request, 'Ruta generada automáticamente con las recomendaciones de IA.')

            return render(request, 'CreateRoute.html', {
                'recommendation3': recommendation3, 
                'form': form, 
                'form_list': form_list, 
                'form_origin_city': form_origin_city, 
                'form_description': form_description
            })
        
    else:
        form = RouteForm()
        form_list=FormRecommendationList()
        form_origin_city = FormRecommendationOriginCity()
        form_description = FormRecommendationDescription()

    return render(request, 'CreateRoute.html', {
        'form': form,
        'form_list':form_list,
        'form_origin_city':form_origin_city,
        'form_description':form_description,
        })  

@require_POST
@login_required
def save_route(request):
    name = request.POST.get('name')
    cities = request.POST.get('cities')
    description = request.POST.get('description')
    estado = request.POST.get('estado', 'private')  # Por defecto en privada

    if Route.objects.filter(name=name).exists():
        messages.error(request, 'Ya existe una ruta con ese nombre. Ingrese otro nombre.')
        return redirect('create_route')

    # Crear la nueva ruta
    route = Route.objects.create(
        user=request.user,
        name=name,
        cities=cities,
        description=description,
        estado=estado,
        is_ai_generated=True
    )
    route.save()
    messages.success(request, 'Recomendación guardada exitosamente.')
    return redirect('user_routes')

@login_required
def user_routes(request):
    routes = Route.objects.filter(user=request.user)

    for route in routes:
        route.cities = ', '.join(route.cities.split(','))
    return render(request, 'user_routes.html', {'routes': routes})

@require_POST
@login_required
def edit_route(request, id):
    route = get_object_or_404(Route, id=id)  # Obtiene la ruta que quieres editar

    if route.user != request.user:
        messages.error(request, "No tienes permiso para modificar esta ruta.")
        return redirect('user_routes')  # O la vista donde se listan las rutas

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)  # Pasa la instancia de la ruta
        if form.is_valid():
            form.save()  # Guarda los cambios
            messages.success(request, 'Ruta editada exitosamente.')
            return redirect('user_routes')  # Redirige a la vista de detalle de la ruta
    else:
        form = RouteForm(instance=route)  # Si no es un POST, crea el formulario con los datos existentes
    return render(request, 'routes/EditRoute.html', {'form': form, 'route': route})  # Renderiza la plantilla

@require_POST
@login_required
def delete_route(request, id):
    route = get_object_or_404(Route, id=id)

    if route.user != request.user:
        messages.error(request, "No tienes permiso para eliminar esta ruta.")
        return redirect('user_routes')
    
    if request.method == "POST":
        route.delete()
        messages.success(request, "Ruta eliminada exitosamente.")
        return redirect('user_routes')  # Cambia esto al nombre de tu vista de rutas
    return redirect('user_routes')  # Opcional, para manejar el caso GET