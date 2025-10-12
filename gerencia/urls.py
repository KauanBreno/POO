from django.urls import path
from django.http import HttpResponse
from .views import home, register, edit_cliente, delete_cliente, cliente, search_clientes

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('edit/<int:pk>/', edit_cliente, name='edit_cliente'),
    path('clientes/<int:pk>/delete/', delete_cliente, name='delete_cliente'),
    path('clientes/<int:pk>/', cliente, name='cliente'),
    path('search-clientes/', search_clientes, name='search_clientes')
]