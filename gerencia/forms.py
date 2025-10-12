import re
from django import forms
from django.forms import inlineformset_factory
from .models import Clientes, Enderecos, Contatos

class ClienteForm(forms.ModelForm):
    
    cnpj = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': 'required', 'pattern': r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', 'placeholder': '00.000.000/0000-00', 'minlength': '18',
        })
    )
    class Meta:
        model = Clientes
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual', 'inscricao_municipal']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-control', 'required minlength': '3', 'maxlength': '100'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control', 'required minlength': '3', 'maxlength': '100'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-control', 'required pattern': '[0-9]{1,30}'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control', 'required pattern': '[0-9]{1,30}'}),    
        }
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        # remove tudo que não for número
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14:
            raise forms.ValidationError("CNPJ deve conter 14 dígitos numéricos.")
        return cnpj

class EnderecoForm(forms.ModelForm):
    
    cep = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': 'required', 'pattern': r'\d{5}-\d{3}', 'placeholder': '00000-000', 'minlength': '9',
            })
    )
    
    uf = forms.CharField(
        max_length=2,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'list': 'uf-list', 'placeholder': 'Ex: SP'}
        )
    )
    class Meta:
        model = Enderecos
        exclude = ('cliente',)
        widgets = {
            'logradoro': forms.TextInput(attrs={'class': 'form-control', 'required minlength': '5', 'maxlength': '150'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '80'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'required minlength': '3', 'maxlength': '70'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'required minlength': '3', 'maxlength': '70'}),
            'uf': forms.Select(attrs={'class': 'form-select', 'required maxlength' :'2', 'minlength': '2', 'pattern':'[A-Za-z]{2}'}),
        }
        
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        # remove tudo que não for número
        cep = re.sub(r'\D', '', cep)
        if len(cep) != 8:
            raise forms.ValidationError("CEP deve conter 8 dígitos numéricos.")
        return cep

class ContatoForm(forms.ModelForm):
    
    telefone = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': 'required', 'pattern': r'\(\d{2}\)\s\d{4}-\d{4}', 'placeholder': '(11) 4444-4444', 'minlength': '14',
        })
    )
    
    celular = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '(11) 98888-8888',
        })
    )
    class Meta:
        model = Contatos
        exclude = ('cliente',)
        widgets = {
            'whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.exemplo.com.br'}),
        }
        
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        telefone = re.sub(r'\D', '', telefone)
        return telefone
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        celular = re.sub(r'\D', '', celular)
        return celular
    
    

EnderecoFormSet = inlineformset_factory(Clientes, Enderecos, form=EnderecoForm, extra=1, can_delete=False)
ContatoFormSet = inlineformset_factory(Clientes, Contatos, form=ContatoForm, extra=1, can_delete=False)
