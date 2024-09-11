from django.urls import path
from django.urls import path, include
from . import views
from city.views import city_reviews

urlpatterns=[
    path('',views.top_250_cities,name='ranking'),
    path('reviews/', include('reviews.urls')),
    path('reviews/<str:city_name>/', city_reviews, name='city_reviews'),
]