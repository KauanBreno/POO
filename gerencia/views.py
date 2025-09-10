from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from.models import Clientes

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST":
        razao_social = request.POST.get('razao_social')
        nome_fantasia= request.POST.get('nome_fantasia')
        cnpj = request.POST.get('cnpj')
        ins_estadual = request.POST.get('ins_estatual')
        ins_municipal = request.POST.get('ins_estatual')
        lagradouro = request.POST.get('logradouro')
        complemento = request.POST.get('complemento')
        bairro = request.POST.get('bairro')
        minicipio = request.POST.get('municipio')
        uf = request.POST.get('uf')
        cep = request.POST.get('cep')
        num_tell = request.POST.get('num_tell')
        num_cell = request.POST.get('celular')
        whatsapp =request.POST.get('whatsapp')
        email = request.POST.get('email')
        url = request.POST.get('url')
