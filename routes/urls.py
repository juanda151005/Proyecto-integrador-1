from django.urls import path
from . import views

urlpatterns=[
    path('',views.route,name='route'),
    path('CreateRoute', views.create_route, name='create_route'),
    path('DeleteRoutes/', views.user_routes, name='user_routes'),
    path('delete/<str:name>/', views.delete_route, name='delete_route'),
]