from django.urls import path
from . import views

urlpatterns=[
    path('',views.route,name='route'),
    path('CreateRoute', views.create_route, name='create_route'),
]