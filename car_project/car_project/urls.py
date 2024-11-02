"""
URL configuration for car_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from car_app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin', admin.site.urls),

    path('', views.user_login,name='Login'),

    path('User_registration', views.user_registration,name="User_registration"),

    path('home_page', views.home_page,name="home_page"),

    path('logout', views.logout, name='logout'),

    path('add_car_for_sale', views.add_car_for_sale, name='add_car_for_sale'),
    path('list_cars_for_sale', views.list_cars_for_sale, name='list_cars_for_sale'),
    path('list_of_my_cars', views.list_my_cars, name='list_of_my_cars'),


    path('add_car_for_rent', views.add_car_for_rent, name='add_car_for_rent'),
    path('list_cars_for_rent', views.list_cars_for_rent, name='list_cars_for_rent'),
    path('list_of_my_cars_for_rent', views.list_my_cars_for_rent, name='list_of_my_cars_for_rent'),

    path('edit_my_cars.html', views.edit_my_cars, name='edit_my_cars'),
    path('edit_my_rent_cars.html', views.edit_my_rent_cars, name='edit_my_rent_cars'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)