from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from validate_docbr import CNPJ
import requests, re

def validar_cnpj(cnpj):
  validatecnpj = CNPJ()
  if not validatecnpj.validate(cnpj):
    raise ValidationError("CNPJ inválido", code="Invalido")

def validar_inscricao_estadual(ie):
  if not re.match(r'^\d{5,20}$', ie):
    raise ValidationError("Inscrição Estadual inválida. Deve conter entre 5 e 20 dígitos numéricos.", code="Invalido")

class Clientes(models.Model):
  nome_fantasia = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
  razao_social = models.CharField(max_length=255, null=False, unique=True, validators=[MinLengthValidator(3)])
  cnpj = models.CharField(max_length=14, unique=True, null=False, blank=False, validators=[validar_cnpj, MinLengthValidator(14, 'CNPJ deve conter exatamente 14 dígitos numéricos.')])
  inscricao_municipal = models.CharField(unique=True, validators=[MinLengthValidator(5)])
  inscricao_estadual = models.CharField(unique=True, validators=[MinLengthValidator(5)])
  data_insercao = models.DateTimeField(auto_now_add=True)
  Ultima_edicao = models.DateTimeField(auto_now=True)

  def clean(self):
    self.nome_fantasia = self.nome_fantasia.title().strip()
    self.razao_social = self.razao_social.title().strip()
    self.cnpj = re.sub(r'\D', '', self.cnpj)
    self.inscricao_municipal = re.sub(r'\D', '', self.inscricao_municipal)
    self.inscricao_estadual = re.sub(r'\D', '', self.inscricao_estadual)

class Enderecos(models.Model):
  uf_choices = [
    ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
    ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
    ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
    ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
    ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
    ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
    ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
  ]

  logradoro = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
  complemento = models.CharField(max_length=255, null=True, blank=True)
  bairro = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
  municipio = models.CharField(max_length=255, null=False, blank=False, validators=[MinLengthValidator(3)])
  uf = models.CharField(max_length=2, choices=uf_choices, validators=[MinLengthValidator(2, 'UF deve conter exatamente 2 letras.')])
  cep = models.CharField(max_length=8, null=False, blank=False, validators=[MinLengthValidator(8, 'CEP deve conter exatamente 8 dígitos numéricos.')])
  cliente = models.OneToOneField(Clientes, on_delete=models.CASCADE, related_name="endereco")

  def clean(self):
    self.logradoro = self.logradoro.title().strip()
    self.complemento = self.complemento.title().strip() if self.complemento else ''
    self.bairro = self.bairro.title().strip()
    self.municipio = self.municipio.title().strip()
    self.uf = self.uf.upper().strip()
    cep = self.cep.replace('-', '').replace('.', '').strip()
    if not re.match(r'^\d{8}$', cep):
      raise ValidationError({'cep': "CEP deve conter exatamente 8 dígitos numéricos."})
    return cep

class Contatos(models.Model):
  telefone = models.CharField(max_length=10, null=False, blank=False, validators=[MinLengthValidator(10, 'Telefone deve conter 10 dígitos numéricos (DDD + número!).')])
  celular = models.CharField(max_length=11, null=True, blank=True)
  whatsapp = models.BooleanField(default=False)
  email = models.EmailField(max_length=100, null=True, blank=True)
  url = models.URLField(max_length=255, null=True, blank=True)
  cliente = models.OneToOneField(Clientes, on_delete=models.CASCADE, related_name="contatos")

  def clean(self):
    if self.telefone:
      self.telefone = re.sub(r'\D', '', self.telefone)
    if self.celular:
      self.celular = re.sub(r'\D', '', self.celular)
    if self.email:
      self.email = self.email.lower()

    if self.whatsapp and not self.celular:
      raise ValidationError("Um número de celular é obrigatório se WhatsApp estiver marcado.")

