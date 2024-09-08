from django.urls import path
from . import views

urlpatterns=[
    path('',views.top_250_cities,name='ranking')
]