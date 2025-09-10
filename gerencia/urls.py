from django.urls import path
from django.http import HttpResponse
from gerencia.views import home

urlpatterns = [
    path('', home, name='home')
]