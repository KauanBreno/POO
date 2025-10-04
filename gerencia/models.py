from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from validate_docbr import CNPJ
import requests, re

def validar_cnpj(cnpj):
        validatecnpj = CNPJ()
        valido = validatecnpj(cnpj)
        if not valido:
            raise ValidationError("CNPJ invalido", code="Invalido")

class Clientes(models.Model):
    nome_fantasia = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
    razao_social = models.CharField(max_length=14, null=False, unique=True, validators=[MinLengthValidator(3)])
    cnpj = models.CharField(max_length=14, unique=True, null=False, blank=False, validators=[validar_cnpj])
    inscricao_minicipal = models.CharField(unique=True, validators=[MinLengthValidator(5)])
    inscricao_estadual = models.CharField(unique=True, validators=[MinLengthValidator(12)])
    data_insercao = models.DateTimeField(auto_now_add=True)
    Ultima_edicao = models.DateTimeField(auto_now=True)        

class Enderecos(models.Model):
    uf_choices = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    logradoro = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
    municipio = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
    uf = models.CharField(max_length=2, choices=uf_choices)
    cep = models.CharField(max_length=8, null=False, blank=False)
    cliente = models.OneToOneField(Clientes, on_delete=models.CASCADE, related_name="endereco")
    
    def clean(self):
        cep = self.cep.replace('-', '').replace('.', '').strip()
        url = f"https://brasilapi.com.br/cep/v2/{cep}"
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            if data["state"] != self.uf:
                raise ValidationError("O UF informado é de um estado diferente do informado no CEP.")
                
        if response.status_code == 400:
            raise ValidationError("CEP Invalido!", code="Invalido")
        if response.status_code == 404:
            raise ValidationError("CEP não Encontrado ou invalido!", code="Not_found")
                
    
class Contatos(models.Model):
    
    telefone = models.CharField(max_length=10, null=False, blank=False, validators=[RegexValidator(r'^\d{10}$', 'Telefone deve ter 10 dígitos (DDD + número).')])
    celular = models.CharField(max_length=11, null=True, blank=True, validators=[RegexValidator(r'^\d{10}$', 'Telefone deve ter 10 dígitos (DDD + número).')])
    whatsapp = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, null=True, blank=True)   
    url = models.URLField(max_length=255, null=True, blank=True)
    cliente = models.OneToOneField(Clientes, on_delete=models.CASCADE, related_name="contatos")
    
    def clean(self):
        if self.whatsapp and not self.celular:
            raise ValidationError("Um número de celular é obrigatório se WhatsApp estiver marcado.")
    
def save(self, *args, **kwargs):
    self.nome_fantasia = " ".join(self.nome_fantasia.split())
    self.razao_social = " ".join(self.razao_social.split())
    self.logradoro = " ".join(self.logradoro.split())
    self.cep = re.sub(r'\D', '', self.cep)
    self.bairro = " ".join(self.bairro.split())
    self.municipio = " ".join(self.municipio.split())
    self.telefone = re.sub(r'\D', '', self.telefone)
    if self.complemento:
        self.complemento = " ".join(self.complemento.split())
    if self.celular:
        self.celular = re.sub(r'\D', '', self.celular)
    if self.email:
        self.email = self.email.lower()
    super().save(*args, **kwargs)