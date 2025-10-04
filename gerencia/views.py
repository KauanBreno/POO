from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from.models import Clientes, Enderecos, Contatos

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST":
            razao_social = request.POST.get('razao_social')
            nome_fantasia= request.POST.get('nome_fantasia')
            cnpj = request.POST.get('cnpj')
            ins_estadual = request.POST.get('ins_estatual')
            ins_municipal = request.POST.get('ins_estatual')
            logradoro = request.POST.get('logradoro')
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
            
            try:
                cliente = Clientes.objects.create(
                    nome_fantasia=nome_fantasia,
                    razao_social=razao_social,
                    cnpj=cnpj,
                    inscricao_estadual=ins_estadual,
                    inscricao_minicipal=ins_municipal
                )
                Enderecos.objects.create(
                    logradoro=logradoro,
                    complemento=complemento,
                    bairro=bairro,
                    municipio=municipio,
                    uf=uf,
                    cep=cep,
                    cliente=cliente
                )
                Contatos.objects.create(
                    telefone=num_tell,
                    celular=num_cell,
                    whatsapp=whatsapp,
                    email=email,
                    url=url,
                    cliente=cliente
                )
                return HttpResponse("Cliente cadastrado com sucesso!")

            except Exception as e:
                return HttpResponse(f"Erro ao cadastrar cliente: {e}", status=400)