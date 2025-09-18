from django.db import models

class Clientes(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=14, unique=True)
    cnpj = models.CharField(max_length=14, unique=True, null=False, blank=False)
    inscricao_minicipal = models.CharField(unique=True, null=False, blank=False)
    inscricao_estadual = models.CharField(unique=True, null=False, blank=False)
    data_insercao = models.DateTimeField(auto_now_add=True)
    Ultima_edicao = models.DateTimeField(auto_now=True)
    endereco = models.OneToOneField(Endereco, models.PROTECT)
    
    
class Endereco(models.Model):
    logradoro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, null=False, blank=False)
    cep = models.CharField(max_length=8, null=False)
    telefone = models.CharField(max_length=11)
    celular = models.CharField(max_length=11)
    whatsapp = models.BooleanField(default=False)
    email = models.EmailField(max_length=100)   
    url = models.CharField(max_length=255)
    
class Contato(models,models):
    telefone = models.CharField(max_length=11)
    celular = models.CharField(max_length=11)
    whatsapp = models.BooleanField(default=False)
    email = models.EmailField(max_length=100)   
    url = models.CharField(max_length=255)
    
