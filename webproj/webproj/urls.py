"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app import views

urlpatterns = [
    #path('', views.index),
    path('movies', views.movies_list),
    path('', views.movies_feed),
    path('news', views.movies_news_feed),
    path('admin/', admin.site.urls),
    path('apply_filters', views.apply_filters),
    path('actors', views.actors_list),
    path('movie/<str:movie>/', views.show_movie, name="show_movie")
]
