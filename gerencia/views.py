from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clientes
from .forms import ClienteForm, EnderecoFormSet, ContatoFormSet
from django.db.models import Q


def home(request):
  query = request.GET.get('q', '')
  clientes = Clientes.objects.select_related('endereco', 'contatos').all()
  if query:
        clientes = clientes.filter(
            Q(nome_fantasia__icontains=query) |
            Q(razao_social__icontains=query) |
            Q(cnpj__icontains=query)
        )
  context = {'clientes': clientes, 'query': query}
  return render(request, 'home.html', context)

def search_clientes(request):
    query = request.GET.get('q', '')  # pega o que foi digitado
    clientes = Clientes.objects.select_related('endereco', 'contatos')

    if query:
        clientes = clientes.filter(
            Q(nome_fantasia__icontains=query) |
            Q(razao_social__icontains=query) |
            Q(cnpj__icontains=query)
        )

    resultados = []

    for c in clientes:
        resultados.append({
            'id': c.id,
            'nome_fantasia': c.nome_fantasia,
            'razao_social': c.razao_social,
            'cnpj': c.cnpj,
            'email': c.contatos.email if hasattr(c, 'contatos') else '',
            'cidade_uf': f"{c.endereco.municipio} / {c.endereco.uf}" if hasattr(c, 'endereco') else '',
        })

    return JsonResponse({'clientes': resultados})

def register(request):
  if request.method == 'POST':
    cliente_form = ClienteForm(request.POST)
    endereco_formset = EnderecoFormSet(request.POST)
    contato_formset = ContatoFormSet(request.POST)

    if not cliente_form.is_valid():
      print("Erros no cliente_form:", cliente_form.errors)
    if not endereco_formset.is_valid():
      print("Erros no endereco_formset:", endereco_formset.errors)
    if not contato_formset.is_valid():
      print("Erros no contato_formset:", contato_formset.errors)

    if cliente_form.is_valid() and endereco_formset.is_valid() and contato_formset.is_valid():
      cliente = cliente_form.save()

      enderecos = endereco_formset.save(commit=False)
      for endereco in enderecos:
        endereco.cliente = cliente
        endereco.save()

      contatos = contato_formset.save(commit=False)
      for contato in contatos:
        contato.cliente = cliente
        contato.save()

      return redirect('cliente', pk=cliente.pk)
  else:
    cliente_form = ClienteForm()
    endereco_formset = EnderecoFormSet()
    contato_formset = ContatoFormSet()

  context = {
    'cliente_form': cliente_form,
    'endereco_formset': endereco_formset,
    'contato_formset': contato_formset,
    'cliente': None,
  }
  return render(request, 'register.html', context)


def edit_cliente(request, pk):
  cliente = get_object_or_404(Clientes, pk=pk)

  if request.method == 'POST':
    cliente_form = ClienteForm(request.POST, instance=cliente)
    endereco_formset = EnderecoFormSet(request.POST, instance=cliente)
    contato_formset = ContatoFormSet(request.POST, instance=cliente)

    if not cliente_form.is_valid():
      print("Erros no cliente_form:", cliente_form.errors)

    if not endereco_formset.is_valid():
        print("Erros no endereco_formset:", endereco_formset.errors)

    if not contato_formset.is_valid():
        print("Erros no contato_formset:", contato_formset.errors)

    if cliente_form.is_valid() and endereco_formset.is_valid() and contato_formset.is_valid():
      cliente = cliente_form.save()
      endereco_formset.instance = cliente
      contato_formset.instance = cliente
      endereco_formset.save()
      contato_formset.save()
      return redirect('cliente', pk=cliente.pk)
    else:
      print("Formulários inválidos")
  else:
    cliente_form = ClienteForm(instance=cliente)
    endereco_formset = EnderecoFormSet(instance=cliente)
    contato_formset = ContatoFormSet(instance=cliente)

  context = {
    'cliente_form': cliente_form,
    'endereco_formset': endereco_formset,
    'contato_formset': contato_formset,
    'cliente': cliente,
  }
  return render(request, 'register.html', context)

def delete_cliente(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    cliente.delete()
    # Se for AJAX, retorna JSON em vez de redirecionar
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('home')


def cliente(request, pk):
  cliente = get_object_or_404(Clientes.objects.select_related('endereco', 'contatos'), pk=pk)
  context = {'cliente': cliente}
  return render(request, 'cliente.html', context)