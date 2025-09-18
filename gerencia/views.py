from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
            logradouro = request.POST.get('logradouro')
            complemento = request.POST.get('complemento')
            bairro = request.POST.get('bairro')
            municipio = request.POST.get('municipio')
            uf = request.POST.get('uf')
            cep = request.POST.get('cep')
            num_tell = request.POST.get('num_tell')
            num_cell = request.POST.get('celular')
            whatsapp =request.POST.get('whatsapp')
            email = request.POST.get('email')
            url = request.POST.get('url')        
            
            cliente = Clientes(
                nome_fantasia = nome_fantasia,
                razao_social = razao_social,
                cnpj = cnpj,
                inscricao_minicipal = ins_estadual,
                inscricao_estadual = ins_municipal,
                logradoro = logradouro,
                complemento = complemento,
                bairro = bairro,
                municipio = municipio,
                uf = uf,
                cep = cep,
                celular = num_cell,
                telefone = num_tell,
                whatsapp = whatsapp,
                email = email,
                url = url
                )
            return HttpResponse("thanks")
        
        
