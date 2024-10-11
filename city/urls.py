from django.urls import path
from . import views

urlpatterns=[
    path('',views.city,name='city'),
    path('city_of_the_day/', views.city_of_the_day, name='city_of_the_day'),
]