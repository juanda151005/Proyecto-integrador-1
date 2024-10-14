from django.urls import path
from . import views

urlpatterns=[
    path('',views.route,name='route'),
    path('CreateRoute', views.create_route, name='create_route'),
    path('DeleteRoutes/', views.user_routes, name='user_routes'),
    path('delete/<int:id>/', views.delete_route, name='delete_route'),
    path('save_route/', views.save_route, name='save_route'),  # guardar rutas
    path('edit_route/<int:id>/', views.edit_route, name='edit_route'),  # editar rutas
]