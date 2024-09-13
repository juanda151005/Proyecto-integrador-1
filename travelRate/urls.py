from django.contrib import admin
from django.urls import path, include
from city import views as cityViews
from city.views import city_reviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cityViews.home, name='home'),
    path('cities/', include('city.urls')),
    path('reviews/', include('reviews.urls')),
    path('reviews/<str:city_name>/', city_reviews, name='city_reviews'),
    path('ranking/', include('ranking.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
