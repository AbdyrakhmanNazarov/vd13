"""
URL configuration for vodorod_cars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import main, car_detail, car_create, car_update, car_delete, about, clients, clients_review


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('cars/<int:id>/', car_detail, name = "car_detail"),
    path('cars_create/', car_create, name='car_create'),    
    path('cars/<int:id>/update', car_update, name = "car_update"),
    path('cars/<int:id>/delete', car_delete, name='car_delete'),
    path('about/', about, name='about'),
    path('clients/', clients, name='clients'),
    path('clients_review/', clients_review, name='clients_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)